from flask import Blueprint, request, abort
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from config import LINE_SECRET
from services.line_service import (reply_message, build_link_success_message,
                                   build_not_found_message)
from repositories.user_repository import is_student_registered, link_line_user

line_bp = Blueprint("line", __name__)
handler = WebhookHandler(LINE_SECRET)


@line_bp.route("/webhook", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body      = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text    = event.message.text.strip()

    if text.isdigit() and len(text) == 10:
        if not is_student_registered(text):
            reply = build_not_found_message()
        else:
            success = link_line_user(text, user_id)
            reply   = build_link_success_message(text) if success else "❌ เกิดข้อผิดพลาด ลองใหม่อีกครั้งครับ"
    else:
        reply = "📌 กรุณาพิมพ์รหัสนักศึกษา 10 หลักเพื่อเชื่อมต่อระบบครับ"

    reply_message(event.reply_token, reply)