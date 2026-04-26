from flask import Blueprint, request, jsonify, make_response
from services.auth_service import verify_login, create_token
from repositories.user_repository import save_user
from middlewares.auth_middleware import token_required
from services.moodle_api_service import fetch_assignments_and_save, login_moodle

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data     = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"error": "กรุณากรอก username และ password"}), 400

    result = verify_login(username, password)
    if not result["status"]:
        return jsonify({"error": result["message"]}), 401

    save_user(
        student_id   = result["username"],
        username     = result["username"],
        display_name = result["DisplayName"]
    )


    login_moodle(username, password)

    token    = create_token(result["username"])
    response = make_response(jsonify({
        "message":      "Login สำเร็จ",
        "username":     result["username"],
        "display_name": result["DisplayName"]
    }))

    response.set_cookie("token", token, httponly=True,
                        max_age=60*60*24*7, samesite="Lax")
    return response, 200


@auth_bp.route("/api/login", methods=["GET"])
@token_required
def check_login():
    return jsonify({
        "message":  "Login อยู่",
        "username": request.current_user
    }), 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logout สำเร็จ"}))
    response.delete_cookie("token")
    return response, 200