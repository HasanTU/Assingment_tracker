import os
from dotenv import load_dotenv

load_dotenv()

# ─── DATABASE ─────────────────────────────────────────────
DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# ─── JWT ──────────────────────────────────────────────────
JWT_SECRET     = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_EXPIRES_DAYS = 7

# ─── LINE ─────────────────────────────────────────────────
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_SECRET       = os.getenv("LINE_SECRET")

# ─── TU API ───────────────────────────────────────────────
TU_API_URL = os.getenv("TU_API_URL", "https://restapi.tu.ac.th/api/v1/auth/Ad/verify")
TU_API_KEY = os.getenv("TU_API_KEY", "")

#
MOODLE_API_URL_LOGIN = os.getenv("MOODLE_API_URL_LOGIN", "https://courses.cs.tu.ac.th/login/token.php") 
MOODLE_API_URL_GET = os.getenv("MOODLE_API_URL_GET", "https://courses.cs.tu.ac.th/webservice/rest/server.php") 

# ─── CORS ─────────────────────────────────────────────────
ALLOWED_ORIGINS = [
    "http://127.0.0.1:5500",
    "http://localhost:5500"
]