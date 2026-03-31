import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

print("DATABASE_URL =", DATABASE_URL)

TU_API_URL = os.getenv('TU_API_URL')
TU_API_APPKEY = os.getenv('TU_API_APPKEY')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60


ORIGIN_WEB_URL = "http://127.0.0.1:3000"
ORIGIN_WEB_URL_2 = ""
BACKEND_WEB_URL = ""

UPLOAD_FOLDER = "uploads"
