from datetime import datetime
from models.assignment import Assignment
from repositories.course_repository import CourseRepository

from models.enums.user_role import UserRole

from models.course import Course

class CourseService:
    def __init__(self, db_session):
        self.course_repe = CourseRepository(db_session)


    def create_course(self, c_name:str, t_id):
        if self.course_repe.get_by_name(c_name): return None
        course = Course(
            course_name = c_name,
            teacher_id = t_id
        )
        return self.course_repe.add(course)
