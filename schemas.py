from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ContactModel(BaseModel):
    email: EmailStr
    phone: str
    note: Optional[str] = None
    user_id: int = Field(1, gt=0)


class ContactResponse(BaseModel):
    id: int = 1
    email: EmailStr
    phone: str
    note: str = None
    user_id: UserResponse

    class Config:
        orm_mode = True
