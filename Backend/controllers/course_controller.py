from flask import Flask, Blueprint, request, jsonify, make_response, g

from services import course_service
from middlewares.auth import role_required

from config import JWT_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from middlewares.auth import token_blacklist

from models.enums.user_role import UserRole

import jwt

course_bp = Blueprint("course", __name__,  url_prefix="/api/courses")


@course_bp.route("/create", methods=["POST"])
@role_required(UserRole.TEACHER)
def create_course():
    data = request.get_json()
    username = g.user["username"]
    user_id = g.user["user_id"]
    role = g.user["role"]

    course_name = data.get("course_name")
    teacher_id = user_id

    course = course_service.create_course(course_name, user_id)
    if not course:
        return jsonify({
            "status": "error",
            "message": f"คอร์สชื่อ '{course_name}' มีอยู่ในระบบแล้ว"
        }), 409 
    
    return jsonify({
        "status": "success",
        "message": "Course created successfully!"
    }), 201



