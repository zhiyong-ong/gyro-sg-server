from __future__ import annotations

from typing import Optional, List

from pydantic.main import BaseModel

from app.core.constants import DrivingLicenceTypeEnum
from app.schemas.bike_availability import BikeAvailability, BikeAvailabilityBase
from app.schemas.bike_model import BikeModel
from app.schemas.user import User


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
    availabilities: Optional[List[BikeAvailabilityBase]] = []


class BikeCreate(BikeBase):
    model_id: int
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
    availabilities: Optional[List[BikeAvailability]] = []

    class Config:
        orm_mode = True
