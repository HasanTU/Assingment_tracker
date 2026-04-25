from database import get_conn


def save_user_task(user_id, assignment_id):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO user_tasks (user_id, assignment_id)
            VALUES (?, ?)
        """, (user_id, assignment_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[TaskRepo] Error: {e}")
        return False
    finally:
        conn.close()


def update_task_status(user_id, assignment_id, status):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE user_tasks
            SET status = ?, last_sync_at = datetime('now', 'localtime')
            WHERE user_id = ? AND assignment_id = ?
        """, (status, user_id, assignment_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"[TaskRepo] Error: {e}")
        return False
    finally:
        conn.close()


def get_pending_notifications():
    """ดึงงานที่ยังไม่แจ้งเตือน และใกล้ครบกำหนด <= 24 ชม."""
    conn = get_conn()
    cursor = conn.cursor()
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
        JOIN users u       ON ut.user_id      = u.user_id
        JOIN assignments a ON ut.assignment_id = a.assignment_id
        WHERE ut.status               = 'pending'
        AND   ut.is_notified          = 0
        AND   u.is_line_notify_active = 1
        AND   u.line_user_id          IS NOT NULL
        AND   a.deadline <= datetime('now', '+1 day', 'localtime')
        AND   a.deadline >= datetime('now', 'localtime')
        ORDER BY a.deadline ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_as_notified(user_task_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_tasks SET is_notified = 1 WHERE user_task_id = ?",
                   (user_task_id,))
    conn.commit()
    conn.close()