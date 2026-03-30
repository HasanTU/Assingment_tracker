from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

from models.enums.user_role import UserRole

from models._base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=True)

    email = Column(String(255), nullable=True)

    role = Column(SQLEnum(UserRole), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())