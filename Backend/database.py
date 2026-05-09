# import sqlite3

from dotenv import load_dotenv
load_dotenv()


from datetime import datetime
from typing import Optional

import pyodbc
from dbutils.pooled_db import PooledDB
import config

CONN_STR = (
    f"DRIVER={{{config.DB_DRIVER}}};"
    f"SERVER={config.DB_SERVER};"
    f"DATABASE={config.DB_NAME};"
    f"UID={config.DB_USER};"
    f"PWD={config.DB_PASSWORD};"
    "TrustServerCertificate=yes;"
)



class PyODBCCreator:
    threadsafety = 1
    Error = pyodbc.Error
    OperationalError = pyodbc.OperationalError

    @staticmethod
    def connect(**kwargs):
        return pyodbc.connect(CONN_STR)

pool = PooledDB(
    creator=PyODBCCreator,
    maxconnections=10,
    mincached=2,
    blocking=True,
    setsession=[],
    ping=1,
    failures=pyodbc.Error,    
    threadsafety=1,         
)

def get_conn():
    return pool.connection()



def row_to_dict(cursor, row) -> Optional[dict]:
    if row is None:
        return None
    cols = [col[0] for col in cursor.description]
    result = {}
    for col, val in zip(cols, row):
        # แปลง datetime object → string ให้เหมือน SQLite เดิม
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
