from dataclasses import dataclass
from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.entities.user import User
from app.utils.project_dependencies import master_database

@dataclass
class UserService:
    db: Session = Depends(master_database)

    def create_user(
        self, name: str, username: EmailStr, password: str, role: str, contact: str
    ) -> User:
        user = User()
        user.name = name
        user.username = username
        user.password = password
        user.role = role
        user.contact = contact
        self.db.add(user)
        self.db.commit()
        return user

    def get_all_users(self):
        return self.db.query(User).all()

    def validate_user(self, username: EmailStr, password: str) -> User | None:
        # this logic should be remvoed once we create some users.
        if self.db.query(User).count() == 0:
            return self.create_user(
                name=username.split("@")[0],
                username=username,
                password=password,
                role="SuperAdmin",
                contact="0987654321",
            )
        user = self.db.query(User).where(User.username == username).first()  # type: ignore
        if user and user.verify_password(password):
            return user
        else:
            return None
