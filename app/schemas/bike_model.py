from __future__ import annotations

from typing import Optional, List

from pydantic.main import BaseModel
from app.schemas.user import User

from app.core.constants import DrivingLicenceTypeEnum


class BikeModelBase(BaseModel):
    name: Optional[str]
    is_deleted: Optional[bool]


class BikeModelCreate(BikeModelBase):
    name: str


class BikeModelUpdate(BikeModelBase):
    pass


class BikeModel(BikeModelBase):
    name: str

    class Config:
        orm_mode = True
