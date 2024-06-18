import json
import os

import google.generativeai as genai
from flask import Flask, jsonify, request, send_file, send_from_directory, Response

API_KEY = 'AIzaSyAxd4beBk62NVDCXvYOSmY_as09n8FwL4U'

# Configure the generative AI with the API key
genai.configure(api_key=API_KEY)

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('web/index.html')

@app.route("/api/chat", methods=["POST"])
def chat():
    if request.method == "POST":
        if API_KEY == 'TODO':
            return jsonify({ "error": 'To get started, get an API key at https://g.co/ai/idxGetGeminiKey and enter it in main.py'.replace('\n', '') })

        try:
            req_body = request.get_json()
            user_message = req_body.get("message")
            model_name = req_body.get("model")

            # Create the generative model instance
            model = genai.GenerativeModel(model_name="gemini-pro")

            # Generate response
            response = model.generate_content(user_message, stream=False)

            return jsonify({ "response": response.text })

        except Exception as e:
            return jsonify({ "error": str(e) })

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(port=int(os.environ.get('PORT', 80)))
