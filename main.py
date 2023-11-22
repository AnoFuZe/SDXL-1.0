from i import HUGGINGFACE_API_KEY
from flask import Flask, render_template, request
import requests
import os
import uuid
import time

app = Flask(__name__)

# Replace 'HUGGINGFACE_API_KEY' with your actual Hugging Face API key
token = HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer " + token}

def query_and_process(description):
    unique_filename = f"result_image_{uuid.uuid4().hex}.png"
    result_image_path = os.path.join(os.path.dirname(__file__), "static", unique_filename)
    payload = {"inputs": description}
    response = requests.post(API_URL, headers=headers, json=payload, stream=True)

    with response, open(result_image_path, "wb") as f:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)

    return unique_filename, "done"

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image_path = None
    progress = None

    if request.method == 'POST':
        description = request.form['description']
        result_image_path, progress = query_and_process(description)

    return render_template('index.html', result_image_path=result_image_path, progress=progress)

if __name__ == '__main__':
    app.run(debug=True)


