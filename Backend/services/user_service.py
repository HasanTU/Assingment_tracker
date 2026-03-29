import requests
from datetime import datetime, timedelta, timezone
from repositories.user_repository import UserRepository
from models.user import User
from models.enums.user_role import UserRole
import jwt
import re

from config import TU_API_URL, TU_API_APPKEY, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES


class UserService:
    def __init__(self, db_session):
        self.user_repo = UserRepository(db_session)
        

    def login_with_tuAPI(self, username: str, password: str):
       
        payload = {"UserName": username, "PassWord": password}
        headers = {"Application-Key": TU_API_APPKEY, "Content-Type": "application/json"}
        response = requests.post(TU_API_URL, json=payload, headers=headers)

        if response.status_code != 200 and response.status_code != 400:
            raise ValueError(response.json())
        elif response.status_code == 400:
            raise ValueError(response.json().get("message"))
        

        user_data = response.json()
        username_from_response = user_data.get("username")
        db_user = self.user_repo.get_by_username(username_from_response)
        
        user_role = None
        if db_user is None:
            user_role = UserRole.STUDENT

            if user_data.get("type") == "employee":
                user_role = UserRole.TEACHER

            db_user = User(
                username=username_from_response,
                role=user_role
            )

            self.user_repo.add(db_user)
        else:
            user_role = db_user.role
        
        displayname_th = user_data.get("displayname_th")

        token = self._create_jwt(db_user.user_id, username_from_response, user_role, displayname_th)
        return token
    

    def login_normal(self, username: str, password: str):
        db_user = self.user_repo.get_by_username(username)

        if db_user is None: raise ValueError("Wrong Username!")
        if db_user.password != password: raise ValueError("Wrong Password!")

        user_role = db_user.role
        
        displayname_th = username + "_Test" + " LastnameTest"
        token = self._create_jwt(db_user.user_id, username, user_role, displayname_th)
        return token

    def _create_jwt(self, user_id, username, role, displayname_th):
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)

        first_name, last_name = self._split_thai_name(displayname_th)

        payload = {
            "user_id": user_id,
            "username": username,
            "first_name":first_name,
            "last_name":last_name,
            "role": role.value,
            "exp": expire
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token
    
    def _split_thai_name(self, fullname):
        if not fullname:
            return "", ""

        parts = re.split(r'\s+', fullname.strip(), maxsplit=1)
        
        first_name = parts[0].strip() if len(parts) > 0 else ""
        last_name = parts[1].strip() if len(parts) > 1 else ""
    
        return first_name, last_name


    def get_user_by_username(self, username:str):
        return self.user_repo.get_by_username(username)

    def get_user_id_by_username(self, username:str):
        user = self.get_user_by_username(username)
        return user if user is None else user.user_id
