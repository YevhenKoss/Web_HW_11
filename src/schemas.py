import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class PersonModel(BaseModel):
    first_name: str
    last_name: str


class PersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ContactModel(BaseModel):
    date_of_birth: datetime.date
    email: EmailStr
    phone: str
    note: Optional[str] = None
    blocked: Optional[bool] = False
    person_id: int = Field(1, gt=0)


class ContactResponse(BaseModel):
    id: int = 1
    date_of_birth: datetime.date
    email: EmailStr
    phone: str
    note: str = None
    blocked: Optional[bool] = False
    person: PersonResponse

    class Config:
        orm_mode = True


class ContactBlackList(BaseModel):
    blocked: Optional[bool] = False

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"