import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

# --- 1. การตั้งค่า (Configuration) ---
# ในสถานการณ์จริง ให้ก๊อปปี้ค่าจากปุ่ม 'AWS Details' ในหน้า Learner Lab มาใส่ตรงนี้
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION = os.getenv("REGION")

def test_upload():
    # สร้างไฟล์ทดสอบเล็กๆ
    test_file_name = "hello_dev1.txt"
    with open(test_file_name, "w") as f:
        f.write("Hello AWS S3! This is a test file from Dev 1.")

    print(f"🚀 กำลังพยายามอัปโหลด {test_file_name} ไปยัง {BUCKET_NAME}...")

    # สร้าง S3 Client ด้วยกุญแจชั่วคราว
    s3 = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=REGION
    )

    try:
        # เริ่มการอัปโหลด
        s3.upload_file(test_file_name, BUCKET_NAME, test_file_name)
        print("✅ สำเร็จ! ไฟล์ของคุณขึ้นไปอยู่บน Cloud เรียบร้อยแล้ว")
        
        # ตรวจสอบว่าไฟล์มีอยู่จริงไหม
        response = s3.head_object(Bucket=BUCKET_NAME, Key=test_file_name)
        print(f"📄 ข้อมูลไฟล์บน S3: ขนาด {response['ContentLength']} bytes")

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '403':
            print("❌ พลาดแล้ว! Error 403: สิทธิ์ (Permissions) ไม่พอ หรือ Token หมดอายุ")
        elif error_code == '404':
            print("❌ ไม่พบ Bucket: ตรวจสอบชื่อ Bucket หรือ Region ให้ถูกต้อง")
        else:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
    except Exception as e:
        print(f"❓ เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
    finally:
        # ลบไฟล์ทดสอบในเครื่องทิ้ง (ทำความสะอาด)
        if os.path.exists(test_file_name):
            os.remove(test_file_name)

if __name__ == "__main__":
    test_upload()