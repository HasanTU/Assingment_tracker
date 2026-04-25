from repositories.user_task_repository import get_pending_notifications, mark_as_notified
from services.line_service import push_message, build_notification_message
import sys
import traceback

print("🚀 notification_service.py เริ่มทำงาน...")

def send_notifications():
    """ดึงงานที่ต้องแจ้งเตือนแล้วส่ง Line"""
    tasks = get_pending_notifications()

    if not tasks:
        print("✅ ไม่มีงานที่ต้องแจ้งเตือนตอนนี้")
        return

    print(f"📋 พบงานที่ต้องแจ้งเตือน {len(tasks)} รายการ")

    for task in tasks:
        message = build_notification_message(task)
        try:
            push_message(task["line_user_id"], message)
            mark_as_notified(task["user_task_id"])
            print(f"✅ ส่งแจ้งเตือนให้ {task['student_id']} — {task['title']}")
        except Exception as e:
            print(f"❌ ส่งไม่ได้ {task['student_id']}: {e}")


if __name__ == "__main__":
    send_notifications()  # <- อย่าลืมเรียกฟังก์ชันหลัก