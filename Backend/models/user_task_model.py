from database import get_conn


def create_user_tasks_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_tasks (
            user_task_id  INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            assignment_id INTEGER NOT NULL,
            status        TEXT DEFAULT 'pending'
                          CHECK(status IN ('pending', 'submitted', 'graded', 'overdue')),
            is_notified   BOOLEAN DEFAULT 0,
            last_sync_at  TIMESTAMP DEFAULT (datetime('now', 'localtime')),
            FOREIGN KEY (user_id)       REFERENCES users(user_id),
            FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id),
            UNIQUE(user_id, assignment_id)
        )
    """)
    conn.commit()
    conn.close()