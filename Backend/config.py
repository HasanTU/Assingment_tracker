import os
from dotenv import load_dotenv

load_dotenv()

# ─── DATABASE ─────────────────────────────────────────────
DB_SERVER   = os.getenv("DB_SERVER")
DB_NAME     = os.getenv("DB_NAME")
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ─── JWT ──────────────────────────────────────────────────
JWT_SECRET       = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
JWT_EXPIRES_DAYS = 7

# ─── LINE ─────────────────────────────────────────────────
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
LINE_SECRET       = os.getenv("LINE_SECRET")

# ─── TU API ───────────────────────────────────────────────
TU_API_URL = os.getenv("TU_API_URL", "https://restapi.tu.ac.th/api/v1/auth/Ad/verify")
TU_API_KEY = os.getenv("TU_API_KEY", "")

# ─── MOODLE ───────────────────────────────────────────────
MOODLE_API_URL_LOGIN = os.getenv("MOODLE_API_URL_LOGIN", "https://courses.cs.tu.ac.th/login/token.php")
MOODLE_API_URL_GET   = os.getenv("MOODLE_API_URL_GET",   "https://courses.cs.tu.ac.th/webservice/rest/server.php")
MOODLE_VIEW_URL      = os.getenv("MOODLE_VIEW_URL",      "https://courses.cs.tu.ac.th/mod/assign/view.php?id=")

# ─── LIFF ─────────────────────────────────────────────────
LIFF_ID = os.getenv("LIFF_ID", "")

# ─── CORS ─────────────────────────────────────────────────
ALLOWED_ORIGINS = [
    "https://rds-db.dyuf0a8afi0ze.amplifyapp.com/",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://4n15xdiqsb.execute-api.us-east-1.amazonaws.com/ "
]
_extra = os.getenv("ALLOWED_ORIGINS")
if _extra:
    ALLOWED_ORIGINS.append(_extra)