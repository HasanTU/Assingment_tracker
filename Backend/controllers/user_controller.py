from flask import Flask, Blueprint, request, jsonify, make_response, g

from services import user_service
from middlewares.auth import role_required

from config import JWT_EXPIRE_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
from middlewares.auth import token_blacklist

from models.enums.user_role import UserRole

import jwt

user_bp = Blueprint("user", __name__,  url_prefix="/api")


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        token = user_service.login_with_tuAPI(username, password)

        response = make_response(jsonify({"message": "login success"}))

        response.set_cookie(
            "token",
            token,
            httponly=False,
            secure=False,
            samesite="Lax",
            max_age=JWT_EXPIRE_MINUTES * 60
        )

        return response
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 401

@user_bp.route("/loginTest", methods=["POST"])
def loginTest():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        token = user_service.login_normal(username, password)

        response = make_response(jsonify({"message": "login success"}))

        response.set_cookie(
            "token",
            token,
            httponly=False,
            secure=False,
            samesite="Lax",
            max_age=JWT_EXPIRE_MINUTES * 60
        )

        return response
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except PermissionError as pe:
        return jsonify({"error": str(pe)}), 401


@user_bp.route("/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token")

    if not token:
        return jsonify({"message": "Already logged out"}), 200

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        exp = payload.get("exp")

        token_blacklist[token] = exp

    except jwt.ExpiredSignatureError:
        pass
    except:
        return jsonify({"error": "Invalid token"}), 401


    response = make_response({"message": "logout"})
    response.set_cookie("token", "", expires=0)
    return response

@user_bp.route("/verify-role", methods=["GET"])
@role_required(UserRole.TEACHER, UserRole.STUDENT)
def verify_role():
    username = g.user["username"]
    role = g.user["role"]

    return jsonify({
        "status": "authenticated",
        "username": username,
        "role": role.value
    }), 200