# sync_handler.py (ประตูหลังบ้านสำหรับ Lambda B)

from services.moodle_api_service import sync_assignments
# สมมติว่าคุณมีฟังก์ชันดึง user ทั้งหมดใน user_repository (ถ้ายังไม่มีต้องไปเขียนเพิ่มนะครับ)
from repositories.user_repository import get_all_users 

def lambda_handler(event, context):
    print("🕒 EventBridge Triggered! เริ่มทำงานแบบ Background Job...")
    
    try:
        # 1. ไปขอดูรายชื่อนักศึกษาทั้งหมดในระบบ (ที่เคยล็อกอินและมี Moodle Token แล้ว)
        users = get_all_users()
        
        if not users:
            print("ไม่พบผู้ใช้งานในระบบที่จะต้อง Sync")
            return "No users to sync"

        success_count = 0
        total_users = len(users)
        
        print(f"👥 พบนักศึกษาทั้งหมด {total_users} คน กำลังเริ่มดึงข้อมูล...")

        # 2. วนลูปสั่ง Sync ทีละคน
        for user in users:
            student_id = user.get("student_id")
            print(f"🔄 กำลัง Sync ของ: {student_id}")
            
            try:
                # เรียกใช้ฟังก์ชันที่คุณส่งมา
                is_success = sync_assignments(student_id)
                if is_success:
                    success_count += 1
            except Exception as e:
                # ถ้าของคนนี้พัง ให้ print บอกไว้ แต่ให้ลูปทำงานต่อของคนถัดไป
                print(f"❌ เกิดข้อผิดพลาดของ {student_id}: {str(e)}")
                continue

        # 3. สรุปผล
        summary = f"✅ Sync Moodle สำเร็จ {success_count}/{total_users} คน"
        print(summary)
        
        # (ออปชันเสริม: เรียก Notify Service ให้ส่ง LINE ไปบอกแอดมินหรือลงกลุ่มว่า Sync เสร็จแล้ว)
        # send_line_notify(summary)
        
        return "Sync Complete"
        
    except Exception as e:
        print(f"❌ System Error (Sync Job Failed): {str(e)}")
        raise e