import os
from sqlalchemy import create_engine

DATABASE_URL = (f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?driver=ODBC+Driver+17+for+SQL+Server")\

TU_API_URL = os.getenv('TU_API_URL')
TU_API_APPKEY = os.getenv('TU_API_APPKEY')

JWT_SECRET_KEY = "no_secret_key_here"
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60

ORIGIN_WEB_URL = "http://127.0.0.1:5500"

UPLOAD_FOLDER = "uploads"
