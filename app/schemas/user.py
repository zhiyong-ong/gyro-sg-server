from typing import Optional

from pydantic import EmailStr
from pydantic.main import BaseModel

from app.core.constants import DrivingLicenceTypeEnum


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    nric_number: Optional[str] = None
    driving_licence_type: Optional[DrivingLicenceTypeEnum] = None

    class Config:
        extra = "forbid"


class UserCreate(UserBase):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    mobile_number: Optional[str] = None
    nric_number: Optional[str] = None
    driving_licence_type: Optional[DrivingLicenceTypeEnum] = None


class UserCreateSuperuser(UserCreate):
    is_superuser: bool = False


class UserUpdateCurrent(UserBase):
    is_active: Optional[bool] = None


class UserUpdatePassword(BaseModel):
    cur_password: str
    new_password: str


class UserUpdateSuperuser(UserUpdateCurrent):
    is_superuser: Optional[bool] = None
    is_active: Optional[bool] = None


class UserUpdateInput(UserUpdateSuperuser):
    password: Optional[str] = None


class User(UserBase):
    is_superuser: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True


class UserWithId(User):
    id: int

    class Config:
        orm_mode = True
