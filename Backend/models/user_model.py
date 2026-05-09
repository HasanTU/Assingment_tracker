from database import get_conn


def create_users_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id               INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id            TEXT UNIQUE NOT NULL,
            username              TEXT,
            display_name          TEXT,
            moodle_API            TEXT,
            moodle_user_id        TEXT,
            line_user_id          TEXT,
            is_line_notify_active BOOLEAN DEFAULT 0,
            last_login            TIMESTAMP,
            created_at            TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()