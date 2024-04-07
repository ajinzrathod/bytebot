from flask import Flask, request, jsonify, render_template
import time
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS
from bs4 import BeautifulSoup
from flask_caching import Cache

from save_data.save_to_md_file import save_to_file
from validations.validate_token import validate_token

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})

# redis configuration
redis_url = os.getenv('REDISCLOUD_URL')
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = redis_url
cache = Cache(app)

# Environmental variables
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
INCUBYTE_BYTEBOT_API_KEY = os.getenv("INCUBYTE_BYTE_BOT_API_KEY")
CLIENT = OpenAI(api_key=INCUBYTE_BYTEBOT_API_KEY)
PROD = int(os.getenv("PROD"))
ASSISTANT_SERVICE_ENABLED = int(os.getenv("ASSISTANT_SERVICE_ENABLED"))
ASK_TOKEN = os.getenv("ASK_TOKEN")
CACHE_TTL = os.getenv("CACHE_TTL")


@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
# @validate_token(ASK_TOKEN)
def ask_incubyte():
    ask_string = os.getenv("ASK_STRING")
    if not ASSISTANT_SERVICE_ENABLED:
        return jsonify({'response': 'We are not serving request at this time'}), 503

    content = request.json.get('question', '')
    if content == '':
        return jsonify({'error': 'No question provided'}), 400

    nocache = "-nocache"
    string_nocache = ask_string + nocache
    if content.lower().startswith(string_nocache):
        ask_string = string_nocache

    soup = BeautifulSoup(content, "html.parser")
    content = ' '.join(soup.get_text().split())
    content = re.sub(re.escape(ask_string), '', content, flags=re.IGNORECASE)

    cache_key = content.lower().strip()
    cached_response = cache.get(cache_key)

    if cached_response and not ask_string.strip().endswith(nocache):
        return jsonify({'response': cached_response, 'cached': True})

    thread = CLIENT.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    run = CLIENT.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    while run.status != "completed":
        run = CLIENT.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    message_response = CLIENT.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    latest_message = messages[0]
    response_text = get_response_text(latest_message, ask_string)

    cache.set(cache_key, response_text, timeout=CACHE_TTL)
    save_to_file(content, response_text)
    return jsonify({'response': response_text, 'cached': False})


def get_response_text(latest_message, ask_string):
    response_text = latest_message.content[0].text.value

    # Remove source information from the response
    response_text = re.sub(r'\【.*?\】', '', response_text)

    # To prevent a continuous loop, remove 'ask string' from the API response
    response_text = re.sub(re.escape(ask_string), '', response_text, flags=re.IGNORECASE)
    return response_text


if __name__ == '__main__':
    if PROD:
        app.run(host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
