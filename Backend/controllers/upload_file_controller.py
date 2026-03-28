from flask import Flask, Blueprint, request, jsonify, make_response, g, current_app

from services import user_service
from middlewares.auth import role_required

from config import JWT_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from middlewares.auth import token_blacklist

from models.enums.user_role import UserRole
from werkzeug.utils import secure_filename

import jwt
import os

upload_file_bp = Blueprint("upload_file", __name__,  url_prefix="/api")


@upload_file_bp.route('/upload', methods=['POST'])
@role_required(UserRole.TEACHER, UserRole.STUDENT)
def upload_file():
    requested_folder = request.form.get('path', 'others')
    safe_folder_name = secure_filename(requested_folder)
    
    # เช็คว่ามีไฟล์มีมั้ย
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    # เช็คว่าชื่อไฟล์ว่างหรือไม่ 
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_folder_name)
        #สร้าง Folder ถ้ายังไม่มี
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
        

        filename = secure_filename(file.filename)
        save_path = os.path.join(target_dir, filename)
        file.save(save_path)

        
        return jsonify({
            "message": "Upload successful!",
            "filename": filename,
            "path": save_path
        }), 200



@upload_file_bp.route('/upload_Old_Ver', methods=['POST'])
def upload_file_old_ver():
    # เช็คว่ามีไฟล์มีมั้ย
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    # 2. เช็คว่าชื่อไฟล์ว่างหรือไม่ 
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # 3. ทำให้ชื่อไฟล์ปลอดภัย 
        filename = secure_filename(file.filename)
        
        # 4. บันทึกไฟล์
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        return jsonify({
            "message": "Upload successful!",
            "filename": filename,
            "path": file_path
        }), 200