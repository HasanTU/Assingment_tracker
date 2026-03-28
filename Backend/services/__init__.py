from database import SessionLocal

from .assignment_service import AssignmentService as AssignmentServiceClass
from .user_service import UserService as UserServiceClass

db_session = SessionLocal()

assignment_service = AssignmentServiceClass(db_session)
user_service = UserServiceClass(db_session)