from datetime import datetime
from models.assignment import Assignment
from repositories.assignment_repository import AssignmentRepository

from services import user_service

class AssignmentService:
    def __init__(self, db_session):
        self.assignment_repo = AssignmentRepository(db_session)

    def create_assignment(self, username: str, title: str, course_id: int, description: str, deadline: datetime):
        user = user_service.get_user_by_username(username)

        if user is None: return

        assignment = Assignment(
            created_by=user.user_id,
            title=title,
            course_id=course_id,
            description=description,
            deadline=deadline
        )
        return self.assignment_repo.add(assignment)
    
    def get_all_by_user_id(self, user_id: int):
        return self.assignment_repo.get_by_user_id(user_id)
