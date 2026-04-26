from flask import Blueprint, jsonify, request
from repositories.assignment_repository import get_all_assignments
from services.user_task_service import get_all_user_tasks_info_by_student_id
from middlewares.auth_middleware import token_required

user_task_bp = Blueprint("user_task", __name__)


@user_task_bp.route("/api/tasks", methods=["GET"])
@token_required
def get_tasks():
    student_id = request.current_user
    tasks = get_all_user_tasks_info_by_student_id(student_id)
    return jsonify({"data": tasks}), 200