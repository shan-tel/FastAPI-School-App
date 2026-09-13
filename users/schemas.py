from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class RoleEnum(str, Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

class UserBase(BaseModel):
    username : str
    email : EmailStr
    full_name : str 
    role : RoleEnum = RoleEnum.student

class UserCreate(UserBase):
    password : str =  Field(min_length = 6)

class UserResponse(UserBase):
    id: int  
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    role: RoleEnum | None = None


