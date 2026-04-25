from config import MOODLE_API_URL_LOGIN, MOODLE_API_URL_GET
from repositories.user_repository import save_moodle_api, get_moodle_user_id_by_student_id, save_moodle_user_id
import requests

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

        res = requests.post(MOODLE_API_URL_LOGIN, data=payload, headers=headers, timeout=10)
        data = res.json()
        if data.get("token"):
            token = data.get("token")
            save_moodle_api(username, token)

            if get_moodle_user_id_by_student_id(username) == None:
                fetch_user_info = fetch_user_info_and_save(token, username).get("status")
                if fetch_user_info.get("status") == False:
                    return fetch_user_info

            return {
                "status": True,
                "token": token,
            }
        
        return {"status": False, "message": data.get("message", "Login ไม่สำเร็จ")}
    except Exception as e:
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
                    courses.insert({
                        "id": course.get("id"),
                        "name": course.get("shortname")
                        })

            return {"status": True, "data": courses}
        
        return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

    except Exception as e:
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}
    

def fetch_assignments_by_course_id(token, course_id):
    try:

        payload = {
            "wstoken": token,
            "wsfunction": "mod_assign_get_assignments",
            "moodlewsrestformat": "json",
            "courseids[0]": course_id
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }



        res = requests.post(MOODLE_API_URL_GET, data=payload, headers=headers, timeout=10)
        data = res.json()

        assignments = []

        if data.get("courses"):
            for course in data.get("courses"):
                if course.get("id"):
                    courses.insert({
                        "id": course.get("id"),
                        "name": course.get("shortname")
                        })

            return {"status": True, "data": courses}
        
        return {"status": False, "message": data.get("message", "ใช้งาน Token ไม่สำเร็จ")}

    except Exception as e:
        return {"status": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}




