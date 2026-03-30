import os
import boto3
from werkzeug.utils import secure_filename
import uuid
from flask import current_app

# โหมดการทำงาน (ดึงจาก .env ถ้าไม่มีให้ใช้ local)
STORAGE_MODE = os.getenv('STORAGE_MODE', 'local') 
S3_BUCKET = os.getenv('S3_BUCKET_NAME')

def get_s3_client():
    """สร้างการเชื่อมต่อกับ AWS S3 โดยใช้ Token จาก Learner Lab"""
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def upload_file_to_cloud(file_object, folder_path):
    """
    รับไฟล์จาก Flask และ Path โฟลเดอร์ แล้วโยนขึ้น S3 หรือ Local ตามการตั้งค่าใน .env
    """
    if not file_object or file_object.filename == '':
        return None

    # 1. จัดการชื่อไฟล์ (ใช้ชื่อเดิม แต่ทำให้ปลอดภัย)
    safe_filename = secure_filename(file_object.filename)
    
    # ผสม UUID เข้าไป 8 ตัวอักษร เพื่อป้องกันนักเรียนส่งไฟล์ชื่อซ้ำกันแล้วเซฟทับกันเอง
    unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_filename}"

    # 2. แยกลอจิกการอัปโหลด
    if STORAGE_MODE == 's3':
        try:
            s3 = get_s3_client()
            
            # สร้าง Path บน S3 เช่น courses/1/assignments/2/1a2b_work.pdf
            # ใช้ .replace("\\", "/") เพื่อป้องกันปัญหา Backslash ตอนรันบน Windows
            s3_key = f"{folder_path}/{unique_filename}".replace("\\", "/") 

            # ยิงไฟล์ขึ้น S3 พร้อมบอกประเภทไฟล์ (เพื่อให้เปิดดูบนเบราว์เซอร์ได้)
            s3.upload_fileobj(
                file_object,
                S3_BUCKET,
                s3_key,
                ExtraArgs={'ContentType': file_object.content_type}
            )
            
            # สร้าง URL เต็มๆ เพื่อส่งกลับไปบันทึกลง Database
            region = os.getenv('AWS_REGION', 'us-east-1')
            url = f"https://{S3_BUCKET}.s3.{region}.amazonaws.com/{s3_key}"
            
            print(f"☁️ [S3] Uploaded success: {url}")
            return url 
            
        except Exception as e:
            print(f"❌ [S3 Error]: {e}")
            return None
            
    else:
        # โหมด Local (ทำงานเหมือนโค้ดเดิมของคุณเป๊ะ เซฟลงโฟลเดอร์ในเครื่อง)
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_path)
        os.makedirs(target_dir, exist_ok=True)
        
        full_path = os.path.join(target_dir, unique_filename)
        file_object.save(full_path)
        
        # คืนค่า Path สั้นๆ สำหรับเซฟลง DB
        db_path = os.path.join(folder_path, unique_filename).replace("\\", "/")
        print(f"💻 [Local] Saved to: {db_path}")
        return db_path