from __future__ import annotations

from typing import Optional, List

from pydantic.main import BaseModel
from app.schemas.user import User
from app.schemas.bike_model import BikeModel

from app.core.constants import DrivingLicenceTypeEnum


class BikeBase(BaseModel):
    color: Optional[str] = None
    required_licence: Optional[DrivingLicenceTypeEnum] = None
    transmission: Optional[str] = None
    storage_box: Optional[bool] = None
    rate: Optional[float] = None
    rate_unit: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    model_id: Optional[int] = None

    class Config:
        extra = "forbid"


class BikeCreateInput(BikeBase):
    model_id: int


class BikeCreate(BikeCreateInput):
    user_id: Optional[int] = None


class BikeUpdate(BikeBase):
    pass


class Bike(BikeBase):
    id: int

    class Config:
        orm_mode = True


class BikeWithRelationships(BikeBase):
    id: int
    model: BikeModel
    user: Optional[User] = None

    class Config:
        orm_mode = True


# BikeWithRelationships.update_forward_refs()
