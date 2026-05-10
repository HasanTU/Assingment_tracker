# lambda_function.py (แพ็กใส่ไฟล์ Zip ของ Lambda A and B)

# นำเข้าตัวแปร app (Flask instance) จากไฟล์ app.py ของคุณ
from app import app 
from mangum import Mangum

# สร้าง handler โดยห่อ Flask app ด้วย Mangum
# Mangum จะทำหน้าที่แปลง Event จาก API Gateway ให้กลายเป็น Flask Request อัตโนมัติ
lambda_handler = Mangum(app)