import sqlite3
from config import DB_PATH


def get_conn():
    """สร้าง Database Connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """สร้างตารางทั้งหมด"""
    from models.user_model import create_users_table
    from models.assignment_model import create_assignments_table
    from models.user_task_model import create_user_tasks_table

    create_users_table()
    create_assignments_table()
    create_user_tasks_table()
