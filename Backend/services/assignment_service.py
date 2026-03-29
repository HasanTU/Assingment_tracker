from datetime import datetime
from models.assignment import Assignment
from repositories.assignment_repository import AssignmentRepository

from models.enums.user_role import UserRole

class AssignmentService:
    def __init__(self, db_session, user_service):
        self.assignment_repo = AssignmentRepository(db_session)

        self.user_service = user_service

    def create_assignment(self, username: str, title: str, course_id: int, description: str, deadline: datetime):
        user = self.user_service.get_user_by_username(username)

        if user is None: return

        assignment = Assignment(
            created_by=user.user_id,
            title=title,
            course_id=course_id,
            description=description,
            deadline=deadline
        )
        return self.assignment_repo.add(assignment)
    
    def get_assignments_by_role(self, user_id, role):
        if role == UserRole.TEACHER:
            # ดูงานที่ตัวเองสร้าง
            return self.assignment_repo.get_all_create_by_user_id(user_id)
        
        elif role == UserRole.STUDENT:
            # ดูงานที่ต้องทำ
            return self.assignment_repo.get_all_doing_by_user_id(user_id)
        
        return None
    
    def get_all_by_user_id(self, user_id: int):
        return self.assignment_repo.get_all_by_user_id(user_id)
    
    
