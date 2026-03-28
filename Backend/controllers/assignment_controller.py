from flask import Blueprint, request, jsonify, g
from middlewares.auth import role_required
from models.enums.user_role import UserRole

from services import assignment_service


assignment_bp = Blueprint("assignment_bp", __name__, url_prefix="/assignments")


@role_required(UserRole.TEACHER)
@assignment_bp.route("", methods=["POST"])
def create_assignment():
    data = request.get_json()
    username = g.user["username"]
    role = g.user["role"]

    title = data.get("title")
    course_id = data.get("course_id")
    description = data.get("description") or ""
    deadline = data.get("deadline")

    return assignment_service.create_assignment(username, title, course_id, description, deadline)


