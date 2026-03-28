from sqlalchemy.orm import Session

from models.user import User

class UserRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_username(self, name: str):
        return self.db.query(User).filter(User.username == name).first()