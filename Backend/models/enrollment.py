from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from models._base import Base


class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id = Column(Integer, primary_key=True, autoincrement=True)

    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)