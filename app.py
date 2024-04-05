from functools import wraps
from flask import Flask, request, jsonify
import time
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS
from bs4 import BeautifulSoup


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

INCUBYTE_BYTEBOT_API_KEY = os.getenv("INCUBYTE_BYTE_BOT_API_KEY")
CLIENT = OpenAI(api_key=INCUBYTE_BYTEBOT_API_KEY)
PROD = int(os.getenv("PROD"))
ASSISTANT_SERVICE_ENABLED = int(os.getenv("ASSISTANT_SERVICE_ENABLED"))
ASK_TOKEN = os.getenv("ASK_TOKEN")
ASK_STRING = os.getenv("ASK_STRING")


@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


@app.route('/')
def index():
    return '<h1>Hi, Welcome to Byte Bot</h1>'


def validate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {ASK_TOKEN}":
            return jsonify({"message": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper


def save_to_file(content, response_text):
    with open("data.md", "a") as file:
        file.write("### Plain Text:\n")
        file.write(f"{content}\n\n")
        file.write("### Response Text:\n")
        file.write(f"{response_text}\n\n")
        file.write("---\n\n")


@app.route('/ask', methods=['POST'])
@validate_token
def ask_incubyte():
    if not ASSISTANT_SERVICE_ENABLED:
        return jsonify({'response': 'We are not serving request at this time'}), 503

    content = request.json.get('question', '')
    if content == '':
        return jsonify({'error': 'No question provided'}), 400

    soup = BeautifulSoup(content, "html.parser")
    content = ' '.join(soup.get_text().split())
    content = re.sub(re.escape(ASK_STRING), '', content, flags=re.IGNORECASE)

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
    response_text = get_response_text(latest_message)
    save_to_file(content, response_text)
    return jsonify({'response': response_text})


def get_response_text(latest_message):
    response_text = latest_message.content[0].text.value

    # Remove source information from the response
    response_text = re.sub(r'\【.*?\】', '', response_text)

    # To prevent a continuous loop, remove 'ask string' from the API response
    response_text = re.sub(re.escape(ASK_STRING), '', response_text, flags=re.IGNORECASE)
    return response_text


if __name__ == '__main__':
    if PROD:
        app.run(host='0.0.0.0', port=5000)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
