# services/auth_service.py
import jwt
import os
import requests
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# 🔑 ใช้จาก .env หรือ config ตามที่คุณถนัด
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
TU_API_URL = os.getenv("TU_API_URL", "https://restapi.tu.ac.th/api/v1/auth/Ad/verify")
TU_API_KEY = os.getenv("TU_API_KEY", "")

# ─── 1. สร้าง JWT Token ─────────────────────────────────────
def create_token(username):
    """สร้าง JWT Token อายุ 7 วัน"""
    payload = {
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# ─── 2. ตรวจสอบการ Login (Mock / Real) ──────────────────────
# 🔹 ใส่โค้ดจาก tu_auth_service.py ของคุณตรงนี้ หรือใช้แบบย่อนี้:
MOCK_USERS = {
    "6512345678": {"password": "password123", "DisplayName": "สมชาย ใจดี"},
    "6709420019": {"password": "mypassword", "DisplayName": "คุณตอร์น เย็น"}
}

def verify_login(username, password):
    """เช็คกับ TU API หรือ Mock"""
    if not username or not password:
        return {"status": False, "message": "กรุณากรอกข้อมูลให้ครบ"}

    # 🟢 ถ้ายังไม่ได้ต่อ TU API จริง → ใช้ Mock
    use_mock = not TU_API_KEY or TU_API_KEY == "your-real-api-key-here"
    
    if use_mock:
        user = MOCK_USERS.get(username)
        if not user:
            return {"status": False, "message": "ไม่พบรหัสนักศึกษานี้ในระบบ"}
        if user["password"] != password:
            return {"status": False, "message": "รหัสผ่านไม่ถูกต้อง"}
        return {
            "status": True,
            "username": username,
            "DisplayName": user["DisplayName"],
            "Email": f"{username}@tu.ac.th"
        }

    # 🔴 ต่อ TU API จริง
    try:
        res = requests.post(TU_API_URL, json={
            "UserName": username, "PassWord": password
        }, headers={"Application-Key": TU_API_KEY}, timeout=10)
        data = res.json()
        if data.get("status"):
            return {
                "status": True,
                "username": data.get("username", username),
                "DisplayName": data.get("displayname_th", ""),
                "Email": data.get("email", "")
            }
        return {"status": False, "message": data.get("message", "Login ไม่สำเร็จ")}
    except Exception as e:
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

# ─── 3. Decorator เช็ค Token (โค้ดเดิมของคุณ) ───────────────
def token_required(f):
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


def get_app_config():
    return {
        "liff_id": os.getenv("LIFF_ID")
    }
