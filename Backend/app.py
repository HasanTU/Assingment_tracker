from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)   
CORS(app)              

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Backend running"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('uploads/' + file.filename)
    return {"message": "uploaded"}

app.run(debug=True)