from flask import Flask, request, jsonify
import time
from openai import OpenAI
import re
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/ask": {"origins": "*"}})
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

incubyte_byte_bot_api_key = os.getenv("INCUBYTE_BYTE_BOT_API_KEY")
client = OpenAI(api_key=incubyte_byte_bot_api_key)
PROD = int(os.getenv("PROD"))
ASSISTANT_SERVICE_ENABLED = int(os.getenv("ASSISTANT_SERVICE_ENABLED"))


@app.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


@app.route('/')
def index():
    return '<h1>Welcome to Byte Bot</h1>'


@app.route('/ask', methods=['POST'])
def ask_incubyte():
    if not ASSISTANT_SERVICE_ENABLED:
        return jsonify({'response': 'We are not serving request at this time'}), 503

    content = request.json.get('question', '')
    if content == '':
        return jsonify({'error': 'No question provided'}), 400

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID,
    )

    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    latest_message = messages[0]
    response_text = latest_message.content[0].text.value

    # Remove source information from the response
    response_text = re.sub(r'\【.*?\】', '', response_text)

    return jsonify({'response': response_text})


if __name__ == '__main__':
    if PROD:
        app.run(host='0.0.0.0', port=80)
    else:
        app.run(debug=True)

