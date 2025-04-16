from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VISION_ENDPOINT = os.getenv("AZURE_ENDPOINT")
VISION_KEY = os.getenv("AZURE_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    image = request.files['image'].read()

    headers = {
        'Ocp-Apim-Subscription-Key': VISION_KEY,
        'Content-Type': 'application/octet-stream'
    }

    params = {
        'visualFeatures': 'Tags'
    }

    response = requests.post(
        f"{VISION_ENDPOINT}/vision/v3.2/analyze",
        headers=headers,
        params=params,
        data=image
    )

    response.raise_for_status()
    analysis = response.json()
    return jsonify(analysis)

if __name__ == '__main__':
    app.run(debug=True)

