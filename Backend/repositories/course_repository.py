from sqlalchemy.orm import Session

from models.course import Course
from models.user import User
from models.enrollment import Enrollment

from models.enums.user_role import UserRole

class CourseRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, course: Course):
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course
    
    def get_by_name(self, name1):
        return self.db.query(Course).filter(Course.course_name.ilike(name1)).first()
    
    def get_all_user_in_course_id(self, course_id):
        users = self.db.query(User).join(
            Enrollment, User.user_id == Enrollment.student_id
            ).filter(
                Enrollment.course_id == course_id,
                User.role == UserRole.STUDENT
            ).all()

        return users