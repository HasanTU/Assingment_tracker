from flask import Flask, Blueprint, request, jsonify, make_response, g, current_app

from services import user_service
from middlewares.auth import role_required

from config import JWT_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from middlewares.auth import token_blacklist

from models.enums.user_role import UserRole
from werkzeug.utils import secure_filename

import jwt
import os

upload_file_bp = Blueprint("upload_file", __name__,  url_prefix="/api/upload")


def save_uploaded_file(file, relative_path):
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # เตรียม Folder
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], relative_path)
    os.makedirs(target_dir, exist_ok=True)

    # Clean ชื่อไฟล์และบันทึก
    filename = secure_filename(file.filename)
    full_path = os.path.join(target_dir, filename)
    file.save(full_path)

    # คืนค่า Path ที่จะเอาไปเก็บใน Database (Relative Path)
    db_path = os.path.join(relative_path, filename)
    
    return jsonify({
        "message": "Upload successful",
        "db_path": db_path,
        "filename": filename
    }), 200


@upload_file_bp.route('/assignment', methods=['POST'])
@role_required(UserRole.TEACHER) 
def upload_assignment_file():
    course_id = request.form.get("course_id")
    assignment_id = request.form.get("assignment_id")

    if not all([course_id, assignment_id]):
        return jsonify({"error": "Missing course_id or assignment_id"}), 400

    # สร้าง Path: courses/{cid}/assignments/{aid}/attachments/
    relative_path = os.path.join("courses", course_id, "assignments", assignment_id, "attachments")
    
    return save_uploaded_file(request.files.get('file'), relative_path)


@upload_file_bp.route('/submission', methods=['POST'])
@role_required(UserRole.STUDENT)
def upload_submission_file():
    course_id = request.form.get("course_id")
    assignment_id = request.form.get("assignment_id")
    student_id = g.user["user_id"] # ดึง ID จาก Token โดยตรง (ปลอดภัยกว่ารับจาก Form)

    if not all([course_id, assignment_id]):
        return jsonify({"error": "Missing course_id or assignment_id"}), 400

    # สร้าง Path: courses/{cid}/assignments/{aid}/submissions/{sid}/
    relative_path = os.path.join("courses", str(course_id), "assignments", str(assignment_id), "submissions", str(student_id))
    
    return save_uploaded_file(request.files.get('file'), relative_path)

@upload_file_bp.route('/other', methods=['POST'])
def upload_other_file():

    # สร้าง Path: other
    relative_path = os.path.join("other")
    
    return save_uploaded_file(request.files.get('file'), relative_path)




# @upload_file_bp.route('/upload_Old_Ver2', methods=['POST'])
# @role_required(UserRole.TEACHER, UserRole.STUDENT)
# def upload_file():
#     requested_folder = request.form.get('path', 'others')
#     safe_folder_name = secure_filename(requested_folder)
    
#     # เช็คว่ามีไฟล์มีมั้ย
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']

#     # เช็คว่าชื่อไฟล์ว่างหรือไม่ 
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if file:
#         target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_folder_name)
#         #สร้าง Folder ถ้ายังไม่มี
#         if not os.path.exists(target_dir):
#             os.makedirs(target_dir, exist_ok=True)
        

#         filename = secure_filename(file.filename)
#         save_path = os.path.join(target_dir, filename)
#         file.save(save_path)

        
#         return jsonify({
#             "message": "Upload successful!",
#             "filename": filename,
#             "path": save_path
#         }), 200



# @upload_file_bp.route('/upload_Old_Ver', methods=['POST'])
# def upload_file_old_ver():
#     # เช็คว่ามีไฟล์มีมั้ย
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']

#     # 2. เช็คว่าชื่อไฟล์ว่างหรือไม่ 
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     if file:
#         # 3. ทำให้ชื่อไฟล์ปลอดภัย 
#         filename = secure_filename(file.filename)
        
#         # 4. บันทึกไฟล์
#         file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)
        
#         return jsonify({
#             "message": "Upload successful!",
#             "filename": filename,
#             "path": file_path
#         }), 200