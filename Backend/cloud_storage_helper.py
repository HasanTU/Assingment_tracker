import os
import boto3
from werkzeug.utils import secure_filename
import uuid
from flask import current_app

def get_s3_client():
    # ดึงค่า Token แบบ Real-time
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
        aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
        region_name=os.getenv('REGION', 'us-east-1')
    )

def upload_file_to_cloud(file_object, folder_path):
    if not file_object or file_object.filename == '':
        return None

    # ดึงค่าจาก .env ตรงนี้ (แทนที่จะดึงจากด้านบนของไฟล์)
    STORAGE_MODE = os.getenv('STORAGE_MODE', 'local') 
    S3_BUCKET = os.getenv('S3_BUCKET_NAME')

    safe_filename = secure_filename(file_object.filename)
    unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_filename}"

    if STORAGE_MODE == 's3':
        try:
            s3 = get_s3_client()
            s3_key = f"{folder_path}/{unique_filename}".replace("\\", "/") 

            s3.upload_fileobj(
                file_object,
                S3_BUCKET,
                s3_key,
                ExtraArgs={'ContentType': file_object.content_type}
            )
            region = os.getenv('AWS_REGION', 'us-east-1')
            url = f"https://{S3_BUCKET}.s3.{region}.amazonaws.com/{s3_key}"
            
            print(f"☁️ [S3] Uploaded success: {url}")
            return url 
            
        except Exception as e:
            print(f"❌ [S3 Error]: {e}")
            return None
            
    else:
        target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], folder_path)
        os.makedirs(target_dir, exist_ok=True)
        
        full_path = os.path.join(target_dir, unique_filename)
        file_object.save(full_path)
        
        db_path = os.path.join(folder_path, unique_filename).replace("\\", "/")
        print(f"💻 [Local] Saved to: {db_path}")
        return db_path