from sqlalchemy.orm import Session

from models.assignment import Assignment
from models.user import User
from models.submission import Submission
from models.course import Course
from models.enrollment import Enrollment

class AssignmentRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, assignment: Assignment):
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)
        return assignment
    
    def get_all_by_user_id(self, user_id):
        return (
            self.db.query(Assignment)
            .filter(Assignment.created_by == user_id)
            .all()
        )
    
    def get_all_doing_by_user_id(self, user_id):
        submitted_ids = self.db.query(Submission.assignment_id).filter(
        Submission.student_id == user_id
        ).subquery()

        doing_assignments = self.db.query(Assignment).join(
            Course, Assignment.course_id == Course.course_id
        ).join(
            Enrollment, Course.course_id == Enrollment.course_id
        ).filter(
            Enrollment.student_id == user_id,
            ~(Assignment.assignment_id.in_(submitted_ids))
        ).all()

        return doing_assignments
    
    def get_all_by_user_id(self, user_id):
        assignments = self.db.query(Assignment).join(
            Course, Assignment.course_id == Course.course_id
        ).join(
            Enrollment, Course.course_id == Enrollment.course_id
        ).filter(
            Enrollment.student_id == user_id,
        ).all()

        return assignments
