from database import get_conn
from repositories.user_repository import get_user_by_student_id
from repositories.assignment_repository import save_assignment
from repositories.user_task_repository import save_user_task
from datetime import datetime, timedelta

# ⚙️ ตั้งค่า: ใส่รหัสนักศึกษาของคุณที่นี่ (หรือรับจาก input)
MY_STUDENT_ID = "6709616459"  # ← แก้เป็นรหัสคุณ

def setup_test_notification(student_id):
    print(f"🔧 กำลังตั้งค่างานทดสอบสำหรับ {student_id}...\n")
    
    # 1. เช็คว่ามีผู้ใช้ในระบบไหม (ต้องล็อกอินผ่านเว็บมาก่อน)
    user = get_user_by_student_id(student_id)
    if not user:
        print(f"❌ ไม่พบผู้ใช้ {student_id} ในฐานข้อมูล")
        print("💡 กรุณา Login ผ่านเว็บก่อน แล้วค่อยรันสคริปต์นี้")
        return False
    
    print(f"✅ พบผู้ใช้: {user.get('display_name') or user['username']}")
    print(f"   LINE ID: {user['line_user_id'][:10] + '...' if user['line_user_id'] else 'ยังไม่ได้ผูก'}")
    print(f"   แจ้งเตือน: {'✅ เปิด' if user['is_line_notify_active'] else '❌ ปิด'}\n")
    
    # 2. ถ้ายังไม่ได้ผูกไลน์ → แจ้งเตือนให้ไปผูกก่อน
    if not user['line_user_id']:
        print("⚠️ คุณยังไม่ได้ผูก LINE กับบัญชีนี้")
        print("📱 กรุณาเพิ่มเพื่อน @assignmenthub แล้วส่งรหัสนักศึกษา 10 หลักเพื่อผูกบัญชี")
        return False
    
    # 3. สร้างงานทดสอบ (deadline อีก 1 ชั่วโมง)
    now = datetime.now()
    deadline = (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"🕒 สร้างงานทดสอบ:")
    print(f"   ⏰ Deadline: {deadline} (อีก 1 ชั่วโมง)")
    
    aid = save_assignment(
        moodle_event_uid=f"test-real-{int(now.timestamp())}",  # UID ไม่ซ้ำ
        title="🧪 [ทดสอบ] แจ้งเตือนงานใกล้ครบ",
        deadline=deadline,
        course_name="ระบบทดสอบอัตโนมัติ",
        course_id="TEST-REAL",
        description="งานนี้สร้างสำหรับทดสอบระบบแจ้งเตือนกับบัญชีจริง",
        source_url="https://moodle.tu.ac.th/assignment/test"
    )
    
    if not aid:
        print("❌ สร้างงานไม่สำเร็จ")
        return False
    
    print(f"✅ สร้างงานสำเร็จ (ID: {aid})")
    
    # 4. เชื่อมผู้ใช้กับงาน (สร้าง user_tasks)
    save_user_task(user['user_id'], aid)
    print(f"✅ เชื่อมงานกับผู้ใช้สำเร็จ")
    
    # 5. รีเซ็ต is_notified = 0 (เพื่อให้แจ้งเตือนได้ แม้เคยรันแล้ว)
    conn = get_conn()
    conn.execute("UPDATE user_tasks SET is_notified = 0 WHERE user_id = ? AND assignment_id = ?", 
                 (user['user_id'], aid))
    conn.commit()
    conn.close()
    print(f"🔄 รีเซ็ตสถานะการแจ้งเตือน (is_notified = 0)")
    
    # 6. สรุป
    print("\n" + "="*60)
    print("✅ ตั้งค่าสำเร็จ! ขั้นตอนต่อไป:")
    print("="*60)
    print("1️⃣  รัน: python notify_bot.py")
    print("2️⃣  เช็คแชทกับบอทใน LINE ของคุณ")
    print("3️⃣  ดู Log ใน Terminal ว่าส่งสำเร็จไหม")
    print("="*60)
    
    return True


if __name__ == "__main__":
   
    setup_test_notification(MY_STUDENT_ID)