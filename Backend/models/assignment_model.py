from database import get_conn
 
 
def create_assignments_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            moodle_event_uid TEXT UNIQUE NOT NULL,
            course_id        TEXT,
            course_name      TEXT,
            title            TEXT NOT NULL,
            description      TEXT,
            source_url       TEXT,
            deadline         DATETIME NOT NULL,
            created_at       TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()
 