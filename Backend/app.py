from database import SessionLocal  # import session factory

from controllers.user_controller import user_bp
from controllers.assignment_controller import assignment_bp
from controllers.upload_file_controller import upload_file_bp
from controllers.course_controller import course_bp

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER

app = Flask(__name__)
db = SessionLocal()

CORS(
    app,
    resources={
    r"/api/*":
    {

        "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
    }
)


app.register_blueprint(user_bp)
app.register_blueprint(assignment_bp)
app.register_blueprint(upload_file_bp)
app.register_blueprint(course_bp)

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response, 200

# ตั้งที้เก็บไฟล์
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "Assignment Hub Backend is running"})

# ย้าย Code Upload ไป upload_file_controller


if __name__ == '__main__':
  
    app.run(debug=True, port=5000)