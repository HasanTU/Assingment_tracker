from config import MOODLE_API_URL_LOGIN, MOODLE_API_URL_GET
from repositories.user_repository import save_moodle_api, get_moodle_user_id_by_student_id, save_moodle_user_id, get_user_by_student_id
from repositories.assignment_repository import bulk_upsert_assignments, save_assignment, get_assignment_by_moodle_id, update_assignment_deadline_and_description, get_assignment_by_assignment_id
from repositories.user_task_repository import save_user_task, update_task_status, get_user_task_by_user_id_and_assignment_id, get_all_user_tasks_by_user_id
from models.enums.task_status import TaskStatus
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from config import MOODLE_VIEW_URL


from datetime import datetime, timezone, timedelta


def convert_moodle_time_to_datetime(ts):
    dt_str = datetime.fromtimestamp(ts, tz=timezone.utc).astimezone(
        timezone(timedelta(hours=7))
    ).strftime("%Y-%m-%d %H:%M:%S")

    return dt_str

def login_moodle(username, password):
    try:
        payload = {
            "username": username,
            "password": password,
            "service": "moodle_mobile_app"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        res = requests.post(MOODLE_API_URL_LOGIN, data=payload, headers=headers, timeout=20)
        data = res.json()


        if data.get("token"):

            token = data.get("token")
            save_moodle_api(username, token)
            moodle_user_id = get_moodle_user_id_by_student_id(username)
            
            first_login = False
            if moodle_user_id is None:
                first_login = True
                fetch_user_info = fetch_user_info_and_save(token, username)

                if fetch_user_info.get("status") == False:
                    return fetch_user_info
                    
                
                fetch_assignments_info = fetch_assignments_and_save(token, username)
                if fetch_assignments_info.get("status") == False:
                        print(fetch_assignments_info)
                        return fetch_assignments_info

            return {
                "status": True,
                "token": token,
                "is_new_user": first_login
            }
        
        return {"status": False, "message": data.get("message", "Login ไม่สำเร็จ")}
    except Exception as e:
        print("เกิดข้อผิดพลาด (login)", e)
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

def fetch_user_info_and_save(token, username):
    try:
        payload = {
            "wstoken": token,
            "wsfunction": "core_webservice_get_site_info",
            "moodlewsrestformat": "json"
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
        data = res.json()
        if data.get("userid"):
            status = save_moodle_user_id(username, data.get("userid"))

            tMessage = "บันทึกสำเร็จ"
            if status == False: tMessage = "บันทึกไม่สำเร็จ"
            
            return {"status": status, "message" : tMessage}
        
        return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

    except Exception as e:
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}



def sync_assignments(student_id):
    user = get_user_by_student_id(student_id)
    if not user: return False

    token = user.get("moodle_API")
    if not token: return False

    fetch_assignments_info = fetch_assignments_and_save(token, student_id)

    if fetch_assignments_info.get("status") == False:
        print(fetch_assignments_info)
        return False
    
    return True


def fetch_assignments_and_save(token, student_id):
    try:
        payload = {
            "wstoken": token,
            "wsfunction": "mod_assign_get_assignments",
            "moodlewsrestformat": "json",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # ✅ ใช้ data= เหมือนเดิม
        res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
        data = res.json()

        if not data.get("courses"):
            return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

        user = get_user_by_student_id(student_id)
        if not user:
            return {"status": False, "message": "ไม่พบ user"}

        user_id = user.get("user_id")

        all_assignments = []
        for course in data.get("courses", []):
            course_id   = course.get("id")
            course_name = course.get("shortname")
            for a in course.get("assignments", []):
                all_assignments.append({
                    "moodle_event_uid": a.get("id"),
                    "title"           : a.get("name"),
                    "deadline"        : convert_moodle_time_to_datetime(a.get("duedate")),
                    "description"     : a.get("intro"),
                    "course_id"       : course_id,
                    "course_name"     : course_name,
                    "source_url"      : MOODLE_VIEW_URL + str(a.get("cmid")),
                })

        assignment_id_map = bulk_upsert_assignments(all_assignments)

        existing_tasks = {
            t["assignment_id"]: t
            for t in get_all_user_tasks_by_user_id(user_id)
        }

        pending_fetches = []
        for a in all_assignments:
            assignment_id = assignment_id_map.get(a["moodle_event_uid"])
            print(f"  uid={a['moodle_event_uid']} → assignment_id={assignment_id}")
            if not assignment_id:
                print("  ⚠️ ข้าม: assignment_id is None")
                continue
            user_task = existing_tasks.get(assignment_id)
            print(f"  user_task={user_task}")
            if user_task and user_task.get("status") == TaskStatus.SUBMITTED.value:
                print("  ⏭️ ข้าม: submitted แล้ว")
                continue
            pending_fetches.append((a["moodle_event_uid"], assignment_id, user_task))
            print(f"  ✅ เพิ่มเข้า pending")

        def fetch_and_save(args):
            moodle_event_uid, assignment_id, user_task = args
            print(f"🔍 fetch: moodle_id={moodle_event_uid} | assignment_id={assignment_id} | user_task={user_task}")
            status = fetch_get_assignment_status(token, moodle_event_uid)
            print(f"   status={status}")
            if user_task is None:
                result = save_user_task(user_id, assignment_id, status)
            else:
                result = update_task_status(user_id, assignment_id, status)
            print(f"   save result={result}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(fetch_and_save, pending_fetches)

        print(f"📋 pending_fetches จำนวน: {len(pending_fetches)}")
        print(f"📋 assignment_id_map: {assignment_id_map}")
        print(f"📋 existing_tasks keys: {list(existing_tasks.keys())}")

        return {"status": True, "data": all_assignments}

    except Exception as e:
        print("เกิดข้อผิดพลาด", e)
        return {"status": False, "message": str(e)}

# def fetch_assignments_and_save(token, student_id):
#     try:
        
#         payload = {
#             "wstoken": token,
#             "wsfunction": "mod_assign_get_assignments",
#             "moodlewsrestformat": "json",
#         }

#         headers = {
#             "Content-Type": "application/x-www-form-urlencoded"
#         }

#         res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
#         data = res.json()

#         assignments = []

#         if not data.get("courses"): return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

#         user = get_user_by_student_id(student_id)
#         if not user: return {"status": False, "message": "ไม่พบ user "}
        
#         user_id = user.get("user_id")

#         for course in data.get("courses"):
#             course_id = course.get("id")
#             course_name = course.get("shortname")

#             for assignment in course.get("assignments"):
#                 moodle_event_uid = assignment.get("id")
#                 description = assignment.get("intro")
#                 deadline = convert_moodle_time_to_datetime(assignment.get("duedate"))
                
#                 title = assignment.get("name")
#                 dataReturn = {}
#                 dataReturn["title"] = title
#                 dataReturn["course_id"] = course_id
#                 dataReturn["deadline"] = deadline
#                 dataReturn["description"] = description

#                 assignment_id = None
#                 if not get_assignment_by_moodle_id(moodle_event_uid):
#                     source_url = MOODLE_VIEW_URL + str(assignment.get("cmid"))

#                     assignment_id = save_assignment(moodle_event_uid, title, deadline, course_id, course_name, description, source_url)
                    
#                 else:
#                     assignment_id = update_assignment_deadline_and_description(moodle_event_uid, deadline, description)
#                     assignment_id = get_assignment_by_moodle_id(moodle_event_uid).get("assignment_id")

#                 assignments.append(dataReturn)

#                 #Sync user task
#                 user_task = get_user_task_by_user_id_and_assignment_id(user_id, assignment_id)
#                 if user_task is None:
#                     print("🔍 [DEBUG] กำลัง fetch:", moodle_event_uid)
#                     status = fetch_get_assignment_status(token, moodle_event_uid)

#                     save_user_task(user_id, assignment_id, status)
                    
#                 else:
#                     if user_task.get("status") == TaskStatus.SUBMITTED.value: continue
#                     print("🔍 [DEBUG] กำลัง fetch:", moodle_event_uid)

#                     status = fetch_get_assignment_status(token, moodle_event_uid)
#                     update_task_status(user_id, assignment_id, status)
    

#         # if student_id:
#         #     if not sync_all_user_tasks(student_id): return {"status": False, "massage": "Fail to sync all user tasks"}


#         return {"status": True, "data": assignments}
        
        
#     except Exception as e:
#         print("เกิดข้อผิดพลาด (fetch assignment and save)", e)
#         return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}

def sync_all_user_tasks(student_id):
    user = get_user_by_student_id(student_id)
    if not user: return False
        

    user_id = user["user_id"]
    token = user["moodle_API"]

    tasks = get_all_user_tasks_by_user_id(user_id)

    for t in tasks:
        if t["status"] == TaskStatus.SUBMITTED.value:
            continue
        assignment = get_assignment_by_assignment_id(t["assignment_id"])
        if not assignment:
            print("MISSING assignment:", t["assignment_id"])

            continue

        status = fetch_get_assignment_status(
            token,
            assignment["moodle_event_uid"]
        )

        update_task_status(user_id, t["assignment_id"], status.value)

    return True




def fetch_get_assignment_status(token, moodle_assignment_id):
    try:
        payload = {
            "wstoken": token,
            "wsfunction": "mod_assign_get_submission_status",
            "moodlewsrestformat": "json",
            "assignid": moodle_assignment_id
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
        data = res.json()

        lastattempt = data.get("lastattempt") or None 

        if not lastattempt: return TaskStatus.PENDING

        sub = lastattempt.get("submission")

        if not sub: return TaskStatus.PENDING

        status = sub.get("status")

        if status == "submitted":
            return TaskStatus.SUBMITTED

        assignment = get_assignment_by_moodle_id(moodle_assignment_id)

        if assignment is None:
            raise ValueError("Assignment not found")
        
        now = datetime.now()
        dt = datetime.strptime(assignment["deadline"], "%Y-%m-%d %H:%M:%S")
        if now > dt:
            return TaskStatus.OVERDUE

        return TaskStatus.PENDING

    except Exception as e:
        print("เกิดข้อผิดพลาด (fetch assignment status)", e)
        return TaskStatus.PENDING


def sync_user_task(token, user_id, assignment_id, moodle_assignment_id):
    user_task = get_user_task_by_user_id_and_assignment_id(user_id, assignment_id)

    if user_task is None:
        save_user_task(user_id, assignment_id)
        
    else:
        if user_task.get("status") == TaskStatus.SUBMITTED.value: return True

        status = fetch_get_assignment_status(token, moodle_assignment_id)
        update_task_status(user_id, assignment_id, status)
    
    return True

def fetch_courses(token, username):
    try:
        moodle_user_id = get_moodle_user_id_by_student_id(username)
        if moodle_user_id == None: return {"status": False, "message": "ดึง user_id ไม่สำเร็จ"}

        payload = {
            "wstoken": token,
            "wsfunction": "core_enrol_get_users_courses",
            "moodlewsrestformat": "json",
            "userid": moodle_user_id
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
        data = res.json()

        courses = []

        if data:
            for course in data:
                if course.get("id"):
                    courses.append({
                        "id": course.get("id"),
                        "name": course.get("shortname")
                        })

            return {"status": True, "data": courses}
        
        return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

    except Exception as e:
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}


    
