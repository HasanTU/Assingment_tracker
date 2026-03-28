from flask import Flask, Blueprint, request, jsonify

from services import user_service


user_bp = Blueprint("user", __name__,  url_prefix="/api")
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        token = user_service.login_with_tuAPI(username, password)
        return jsonify({"access_token": token})
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 401