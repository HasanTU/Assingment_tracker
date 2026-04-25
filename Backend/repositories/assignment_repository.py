from database import get_conn

# repositories/assignment_repository.py
def save_assignment(moodle_event_uid, title, deadline,
                    course_id=None, course_name=None,
                    description=None, source_url=None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        print(f"🔍 [DEBUG] กำลังบันทึก: {moodle_event_uid}")
        cursor.execute("""
            INSERT OR IGNORE INTO assignments
            (moodle_event_uid, course_id, course_name, title, description, source_url, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (moodle_event_uid, course_id, course_name, title, description, source_url, deadline))
        
        print(f"📊 [DEBUG] Rows affected: {cursor.rowcount}")  # 0 = ข้อมูลซ้ำ, 1 = ใหม่
        conn.commit()
        print("✅ [DEBUG] Commit สำเร็จ!")
        
        cursor.execute("SELECT assignment_id FROM assignments WHERE moodle_event_uid = ?", (moodle_event_uid,))
        row = cursor.fetchone()
        return row["assignment_id"] if row else None
    except Exception as e:
        print(f"💥 [DEBUG] ERROR: {type(e).__name__}: {e}")
        return None
    finally:
        conn.close()


def get_all_assignments():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assignments ORDER BY deadline ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]