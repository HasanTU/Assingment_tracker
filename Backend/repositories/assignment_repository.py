from database import get_conn, row_to_dict



# repositories/assignment_repository.py
def save_assignment(moodle_event_uid, title, deadline,
                    course_id=None, course_name=None,
                    description=None, source_url=None):
    conn = get_conn()
    cursor = conn.cursor()
    try:
        print(f"🔍 [DEBUG] กำลังบันทึก: {moodle_event_uid}")

        # MSSQL ไม่มี INSERT OR IGNORE → ใช้ IF NOT EXISTS แทน
        cursor.execute("""
            IF NOT EXISTS (
                SELECT 1 FROM assignments WHERE moodle_event_uid = ?
            )
            INSERT INTO assignments
                (moodle_event_uid, course_id, course_name, title,
                 description, source_url, deadline)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (moodle_event_uid,                          # สำหรับ NOT EXISTS
              moodle_event_uid, course_id, course_name,  # สำหรับ INSERT
              title, description, source_url, deadline))

        print(f"📊 [DEBUG] Rows affected: {cursor.rowcount}")  # 0 = ซ้ำ, 1 = ใหม่
        conn.commit()
        print("✅ [DEBUG] Commit สำเร็จ!")

        cursor.execute(
            "SELECT assignment_id FROM assignments WHERE moodle_event_uid = ?",
            (moodle_event_uid,)
        )
        row = cursor.fetchone()
        return row[0] if row else None  # pyodbc ใช้ index แทน key

    except Exception as e:
        print(f"💥 [DEBUG] ERROR: {type(e).__name__}: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def update_assignment_deadline_and_description(moodle_event_uid, deadline, description):
    if deadline is None or description is None:
        return None

    conn = get_conn()
    cursor = conn.cursor()
    try:
        # ใช้ OUTPUT clause เพื่อดึง assignment_id หลัง UPDATE ใน statement เดียว
        cursor.execute("""
            UPDATE assignments
            SET deadline = ?, description = ?
            OUTPUT INSERTED.assignment_id
            WHERE moodle_event_uid = ?
              AND (
                    deadline    IS NULL OR deadline    != ?
                OR  description IS NULL OR description != ?
              )
        """, (deadline, description, moodle_event_uid, deadline, description))

        row = cursor.fetchone()
        conn.commit()
        return row[0] if row else None

    except Exception as e:
        print(f"💥 [DEBUG] ERROR: {type(e).__name__}: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()


def get_assignment_by_moodle_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM assignments WHERE moodle_event_uid = ?", (id,)
    )
    row = cursor.fetchone()
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def get_assignment_by_assignment_id(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM assignments WHERE assignment_id = ?", (id,)
    )
    row = cursor.fetchone()
    result = row_to_dict(cursor, row)
    conn.close()
    return result


def get_all_assignments():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assignments ORDER BY deadline ASC")
    rows = cursor.fetchall()
    result = [row_to_dict(cursor, r) for r in rows]
    conn.close()
    return result

def bulk_upsert_assignments(assignments: list) -> dict:
    if not assignments:
        print("⚠️ assignments ว่างเปล่า!")
        return {}

    conn = get_conn()
    cursor = conn.cursor()
    result = {}

    try:
        for a in assignments:
            cursor.execute("""
                MERGE assignments AS target
                USING (SELECT ? AS moodle_event_uid) AS source
                ON target.moodle_event_uid = source.moodle_event_uid
                WHEN MATCHED AND (
                    target.deadline != ? OR target.description != ?
                ) THEN
                    UPDATE SET deadline = ?, description = ?
                WHEN NOT MATCHED THEN
                    INSERT (moodle_event_uid, course_id, course_name,
                            title, description, source_url, deadline)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                a["moodle_event_uid"],
                a["deadline"], a["description"],
                a["deadline"], a["description"],
                a["moodle_event_uid"], a["course_id"],
                a["course_name"], a["title"],
                a["description"], a["source_url"], a["deadline"]
            ))

        conn.commit()
        print("✅ commit สำเร็จ")

        uids = [a["moodle_event_uid"] for a in assignments]
        placeholders = ",".join(["?"] * len(uids))
        cursor.execute(
            f"SELECT moodle_event_uid, assignment_id FROM assignments WHERE moodle_event_uid IN ({placeholders})",
            uids
        )
        rows = cursor.fetchall()
        print(f"📊 ดึงกลับได้ {len(rows)} rows")
        for row in rows:
            result[int(row[0])] = row[1]  # ✅ แก้ตรงนี้

    except Exception as e:
        print(f"💥 ERROR: {type(e).__name__}: {e}")
        conn.rollback()
    finally:
        conn.close()

    return result