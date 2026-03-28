from sqlalchemy.orm import Session

from models.assignment import Assignment
from models.user import User

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