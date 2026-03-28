from functools import wraps
from flask import request, jsonify, g
import jwt
import time

from models.enums.user_role import UserRole

from config import JWT_ALGORITHM, JWT_SECRET_KEY


token_blacklist = {}

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.cookies.get("token")
            #token = request.headers.get("Authorization")

            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                #token = token.split(" ")[1]

                clean_blacklist()

                if token in token_blacklist:
                    if token_blacklist[token] > time.time():
                        return jsonify({"error": "Logged out"}), 401
                    else:
                        del token_blacklist[token]

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
            
            if not hasattr(g, "user") or g.user is None:
                return jsonify({"error": "User not authenticated"}), 401

            return f(*args, **kwargs)

        return decorated
    return decorator


def clean_blacklist():
    now = time.time()
    expired_tokens = [t for t, exp in token_blacklist.items() if exp < now]
    
    for t in expired_tokens:
        del token_blacklist[t]