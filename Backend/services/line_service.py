from linebot import LineBotApi
from linebot.models import TextSendMessage
from config import LINE_ACCESS_TOKEN

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)


def reply_message(reply_token, text):
    """ตอบกลับข้อความใน Line"""
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))


def push_message(line_user_id, text):
    """ส่งข้อความหา user โดยตรง"""
    line_bot_api.push_message(line_user_id, TextSendMessage(text=text))


def build_link_success_message(student_id):
    return (
        f"✅ เชื่อมต่อสำเร็จ!\n"
        f"รหัส {student_id} ผูกกับ Line แล้ว\n"
        f"ระบบจะแจ้งเตือนงานมาที่นี่ครับ 📚"
    )


def build_not_found_message():
    return (
        "❌ ไม่พบรหัสนักศึกษานี้ในระบบ\n"
        "กรุณา Login ผ่านเว็บก่อน แล้วค่อยส่งรหัสมาครับ"
    )


def build_notification_message(task):
    msg = (
        f"📢 แจ้งเตือนงานใกล้ครบกำหนด!\n"
        f"วิชา: {task['course_name']}\n"
        f"งาน: {task['title']}\n"
        f"⏳ Deadline: {task['deadline']}\n"
    )
    if task.get("source_url"):
        msg += f"🔗 {task['source_url']}\n"
    msg += "อย่าลืมส่งนะครับ!"
    return msg