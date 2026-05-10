# lambda_function.py

from app import app
from mangum import Mangum
from asgiref.wsgi import WsgiToAsgi

# 1. แปลง Flask (รุ่นเก๋า) ให้เป็น ASGI (รุ่นใหม่)
asgi_app = WsgiToAsgi(app)

# 2. ให้ Mangum เข้ามาห่อโค้ดที่แปลงแล้ว 
lambda_handler = Mangum(asgi_app, lifespan="off")