from enum import Enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, description="Password must be at least 4 characters")
    role: UserRoleEnum = UserRoleEnum.user  


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=4)
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    role: UserRoleEnum
    is_active: bool

    class Config:
        from_attributes = True