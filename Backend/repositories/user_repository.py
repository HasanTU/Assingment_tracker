from database import get_conn


def save_user(student_id, username=None, display_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (student_id, username, display_name, last_login)
            VALUES (?, ?, ?, datetime('now', 'localtime'))
            ON CONFLICT(student_id) DO UPDATE SET
                username     = excluded.username,
                display_name = excluded.display_name,
                last_login   = datetime('now', 'localtime')
        """, (student_id, username, display_name))
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        return False
    finally:
        conn.close()


def link_line_user(student_id, line_user_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET line_user_id = ?, is_line_notify_active = 1
            WHERE student_id = ?
        """, (line_user_id, student_id))
        updated = cursor.rowcount > 0
        conn.commit()
        return updated
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        return False
    finally:
        conn.close()

def save_moodle_user_id(student_id, moodle_user_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET moodle_user_id = ? WHERE student_id = ?",
                       (moodle_user_id, student_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        return False
    finally:
        conn.close()



def save_moodle_api(student_id, moodle_api):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET moodle_API = ? WHERE student_id = ?",
                       (moodle_api, student_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        return False
    finally:
        conn.close()


def get_moodle_user_id_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT moodle_user_id FROM users WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_user_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE student_id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_all_users():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def is_student_registered(student_id):
    return get_user_by_student_id(student_id) is not None