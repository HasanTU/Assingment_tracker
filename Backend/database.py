import os
import pymssql
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional

load_dotenv()

import config

# Local → ใช้ค่าจาก config/.env
# Lambda → ใช้ค่าจาก Environment Variables (os.environ)
DB_SERVER   = os.environ.get("DB_SERVER",   config.DB_SERVER)
DB_NAME     = os.environ.get("DB_NAME",     config.DB_NAME)
DB_USER     = os.environ.get("DB_USER",     config.DB_USER)
DB_PASSWORD = os.environ.get("DB_PASSWORD", config.DB_PASSWORD)

pool = PooledDB(
    creator=pymssql,
    maxconnections=10,
    mincached=2,
    blocking=True,
    host=DB_SERVER,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
)

def get_conn():
    return pool.connection()

def row_to_dict(cursor, row) -> Optional[dict]:
    if row is None:
        return None
    cols = [col[0] for col in cursor.description]
    result = {}
    for col, val in zip(cols, row):
        if isinstance(val, datetime):
            result[col] = val.strftime("%Y-%m-%d %H:%M:%S")
        else:
            result[col] = val
    return result
# def get_conn():
#     conn = pyodbc.connect(
#         f"DRIVER={{{config.DB_DRIVER}}};"
#         f"SERVER={config.DB_SERVER};"
#         f"DATABASE={config.DB_NAME};"
#         f"UID={config.DB_USER};"
#         f"PWD={config.DB_PASSWORD}"
#     )
#     return conn


# def get_conn():
#     """สร้าง Database Connection"""
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     """สร้างตารางทั้งหมด"""
#     from models.user_model import create_users_table
#     from models.assignment_model import create_assignments_table
#     from models.user_task_model import create_user_tasks_table

#     create_users_table()
#     create_assignments_table()
#     create_user_tasks_table()
