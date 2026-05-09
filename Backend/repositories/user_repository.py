from database import get_conn, row_to_dict


# repositories/user_repository.py
def save_user(student_id, username=None, display_name=None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # SQLite ใช้ ON CONFLICT → MSSQL ใช้ MERGE แทน (UPSERT)
        cursor.execute("""
            MERGE INTO users AS target
            USING (VALUES (?, ?, ?)) AS source (student_id, username, display_name)
                ON target.student_id = source.student_id
            WHEN MATCHED THEN
                UPDATE SET
                    username     = source.username,
                    display_name = source.display_name,
                    last_login   = GETDATE()
            WHEN NOT MATCHED THEN
                INSERT (student_id, username, display_name, last_login)
                VALUES (source.student_id, source.username, source.display_name, GETDATE());
        """, (student_id, username, display_name))
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        conn.rollback()
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
        conn.rollback()
        return False
    finally:
        conn.close()


def save_moodle_user_id(student_id, moodle_user_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET moodle_user_id = ? WHERE student_id = ?",
            (moodle_user_id, student_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def save_moodle_api(student_id, moodle_api):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET moodle_API = ? WHERE student_id = ?",
            (moodle_api, student_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"[UserRepo] Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_moodle_token_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT moodle_API FROM users WHERE student_id = ?", (student_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_moodle_user_id_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT moodle_user_id FROM users WHERE student_id = ?", (student_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def get_user_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE student_id = ?", (student_id,)
    )
    row = cursor.fetchone()
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def get_all_users():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result


def is_student_registered(student_id):
    return get_user_by_student_id(student_id) is not None