import jwt
from functools import wraps
from flask import request, jsonify
from config import JWT_SECRET


def token_required(f):
    """Decorator เช็ค JWT Token ก่อนเข้า route"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return jsonify({"error": "ไม่มี token กรุณา Login ก่อน"}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.current_user = payload["username"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token หมดอายุ กรุณา Login ใหม่"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token ไม่ถูกต้อง"}), 401

        return f(*args, **kwargs)
    return decorated