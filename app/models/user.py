from sqlalchemy import Boolean, Column, String, Integer, Enum
from app.database import Base
from app.schemas.user import UserRoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.user)
    is_active = Column(Boolean, default=True)