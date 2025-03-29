from app import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.responses import UserRoleResponse

class UserRole(db.Model):
    __tablename__ = "user_role"

    role_id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Roles {self.name}>"

    @staticmethod
    def get_all_roles():
        roles = UserRole.query.all()
        return UserRoleResponse.response_all_roles(roles)