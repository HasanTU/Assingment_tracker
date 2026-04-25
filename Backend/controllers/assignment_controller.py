from flask import Blueprint, jsonify, request
from repositories.assignment_repository import get_all_assignments
from repositories.user_task_repository import get_pending_notifications
from middlewares.auth_middleware import token_required

assignment_bp = Blueprint("assignment", __name__)


@assignment_bp.route("/api/assignments", methods=["GET"])
@token_required
def get_assignments():
    assignments = get_all_assignments()
    return jsonify({"assignments": assignments}), 200


@assignment_bp.route("/api/notifications/pending", methods=["GET"])
@token_required
def get_pending():
    tasks = get_pending_notifications()
    return jsonify({"tasks": tasks}), 200