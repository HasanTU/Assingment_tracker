from database import get_conn, row_to_dict

def get_all_user_tasks_by_user_id(user_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ut.*,
            a.deadline
        FROM user_tasks ut
        JOIN assignments a ON ut.assignment_id = a.assignment_id
        WHERE ut.user_id = ?
        ORDER BY a.deadline ASC
    """, (user_id,))
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result


def get_all_user_tasks_by_user_id_and_course_id(user_id, course_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ut.*,
            a.deadline
        FROM user_tasks ut
        JOIN assignments a ON ut.assignment_id = a.assignment_id
        WHERE ut.user_id = ?
          AND a.course_id = ?
        ORDER BY a.deadline ASC
    """, (user_id, course_id))
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result


def get_user_task_by_user_id_and_assignment_id(user_id, assignment_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM user_tasks
        WHERE user_id = ? AND assignment_id = ?
    """, (user_id, assignment_id))
    row = cursor.fetchone()
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def get_all_user_task_and_assignment_info_by_student_id(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ut.assignment_id,
            ut.status,
            a.course_name,
            a.title,
            a.description,
            a.source_url,
            a.deadline
        FROM users u
        JOIN user_tasks  ut ON u.user_id       = ut.user_id
        JOIN assignments a  ON ut.assignment_id = a.assignment_id
        WHERE u.student_id = ?
        ORDER BY a.deadline ASC
    """, (student_id,))
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result


def save_user_task(user_id, assignment_id, status="pending"):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # INSERT OR IGNORE → IF NOT EXISTS INSERT
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM user_tasks
                WHERE user_id = ? AND assignment_id = ?
            )
            INSERT INTO user_tasks (user_id, assignment_id, status)
            VALUES (?, ?, ?)
        """, (user_id, assignment_id,   # สำหรับ NOT EXISTS
              user_id, assignment_id, status))
        conn.commit()
        return True
    except Exception as e:
        print(f"[TaskRepo] Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def update_task_status(user_id, assignment_id, status):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        # datetime('now', 'localtime') → GETDATE()
        cursor.execute("""
            UPDATE user_tasks
            SET status = ?, last_sync_at = GETDATE()
            WHERE user_id = ? AND assignment_id = ?
        """, (status, user_id, assignment_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[TaskRepo] Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def get_pending_notifications():
    """ดึงงานที่ยังไม่แจ้งเตือน และใกล้ครบกำหนด <= 24 ชม."""
    conn = get_conn()
    cursor = conn.cursor()
    # datetime('now', '+1 day', 'localtime') → DATEADD(day, 1, GETDATE())
    cursor.execute("""
        SELECT
            u.line_user_id,
            u.student_id,
            a.title,
            a.course_name,
            a.deadline,
            a.source_url,
            ut.user_task_id
        FROM user_tasks ut
        JOIN users       u ON ut.user_id      = u.user_id
        JOIN assignments a ON ut.assignment_id = a.assignment_id
        WHERE ut.status               = 'pending'
          AND ut.is_notified          = 0
          AND u.is_line_notify_active = 1
          AND u.line_user_id          IS NOT NULL
          AND a.deadline <= DATEADD(day, 1, GETDATE())
          AND a.deadline >= GETDATE()
        ORDER BY a.deadline ASC
    """)
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result


def mark_as_notified(user_task_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_tasks SET is_notified = 1 WHERE user_task_id = ?",
        (user_task_id,)
    )
    conn.commit()
    conn.close()