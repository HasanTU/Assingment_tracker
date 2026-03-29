from flask import Blueprint, request, jsonify, g
from middlewares.auth import role_required
from models.enums.user_role import UserRole

from services import assignment_service, user_service
from config import ORIGIN_WEB_URL

assignment_bp = Blueprint("assignment_bp", __name__, url_prefix="/api/assignments")


@assignment_bp.route("/create", methods=["POST"])
@role_required(UserRole.TEACHER)
def create_assignment():
    data = request.get_json()
    username = g.user["username"]
    role = g.user["role"]

    title = data.get("title")
    course_name = data.get("course_name")
    description = data.get("description") or ""
    deadline = data.get("deadline")

    assignment = assignment_service.create_assignment(username, title, course_name, description, deadline)
    assignment_id = assignment.assignment_id
    course_id = assignment.course_id
    return jsonify({
        "status": "success",
        "message": "Assignment created successfully!",
        "data": {
            "assignment_id":assignment_id,
            "course_id":course_id
        }
    }), 201

@assignment_bp.route("", methods=["GET"])
@role_required(UserRole.TEACHER, UserRole.STUDENT)
def get_assignments():
    username = g.user["username"]
    role = g.user["role"]
    user_id = g.user["user_id"] #user_service.get_user_id_by_username(username)
    
    if user_id is None:
        return jsonify({
            "status": "error",
            "message": "No User Id!"
        }), 404

    assignments = assignment_service.get_assignments_by_role(user_id, role)

    assignments_list = [
        {
            "id": a.assignment_id,
            "title": a.title,
            "course_id": a.course_id,
            "deadline": a.deadline.isoformat() if a.deadline else None
        } for a in assignments
    ]
    
    return jsonify({
        "status": "success",
        "data": assignments_list
    }), 200



