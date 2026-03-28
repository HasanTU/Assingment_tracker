from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from models.user import User
from models.course import Course
from models.assignment import Assignment
from models.submission import Submission
from models.enrollment import Enrollment

from config import DATABASE_URL

from models._base import Base



engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(engine)