from functools import wraps
from flask import request, jsonify, g
import jwt

from models.enums.user_role import UserRole

from config import JWT_ALGORITHM, JWT_SECRET_KEY


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")

            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                token = token.split(" ")[1]
                data = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)

                try:
                    user_role = UserRole(data.get("role"))
                except ValueError:
                    return jsonify({"error": "Invalid role"}), 400

                if user_role not in roles:
                    return jsonify({"error": "Forbidden"}), 403

                g.user = {
                    "user_id": data.get("user_id"),
                    "username": data.get("username"),
                    "role": user_role
                }
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401

            except:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)

        return decorated
    return decorator