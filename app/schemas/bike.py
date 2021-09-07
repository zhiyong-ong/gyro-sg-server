from __future__ import annotations

from typing import Optional, List, Any

from pydantic.main import BaseModel

from app.schemas.bike_availability import BikeAvailability, BikeAvailabilityBase
from app.schemas.bike_model import BikeModel
from app.schemas.licence_class import LicenceClass
from app.schemas.transmission import Transmission
from app.schemas.user import User


class BikeBase(BaseModel):
    color: Optional[str] = None
    storage_rack: Optional[bool] = None
    storage_box: Optional[bool] = None
    rate: Optional[float] = None
    rate_unit: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    licence_class_id: Optional[int] = None
    transmission_id: Optional[int] = None
    model_id: Optional[int] = None



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


class BikeResponse(BaseModel):
    id: int
    color: Optional[str] = None
    storage_rack: Optional[bool] = None
    storage_box: Optional[bool] = None
    rate: Optional[float] = None
    rate_unit: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    model: BikeModel
    licence_class: Optional[LicenceClass] = None
    transmission: Optional[Transmission] = None
    user: Optional[User] = None
    availabilities: Optional[List[BikeAvailability]] = []

    class Config:
        orm_mode = True

class FilterResponse(BaseModel):
    header: str
    fields: List[Any]

class LicenceClassFilterResponse(FilterResponse):
    fields: List[LicenceClass]

class TransmissionFilterResponse(FilterResponse):
    fields: List[Transmission]

class Other(BaseModel):
    name: Optional[str]
    description: Optional[str]

class OtherFilterResponse(FilterResponse):
    fields: List[Other]

class BikeFilterParams(BaseModel):
    licence_class: LicenceClassFilterResponse
    transmission: TransmissionFilterResponse
    other: OtherFilterResponse
