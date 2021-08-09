from __future__ import annotations

from datetime import datetime

from pydantic import validator
from pydantic.main import BaseModel


class BikeAvailabilityBase(BaseModel):
    start_datetime: datetime
    end_datetime: datetime

    @validator("start_datetime", "end_datetime")
    def validate_datetime_timezone_aware(cls, v, field):
        if v.tzinfo is not None and v.tzinfo.utcoffset(v) is not None:
            return v
        else:
            raise ValueError(f"{field} must be timezone aware")


class BikeAvailabilityCreate(BikeAvailabilityBase):
    bike_id: int


class BikeAvailabilityUpdate(BikeAvailabilityBase):
    pass


class BikeAvailability(BikeAvailabilityBase):
    class Config:
        orm_mode = True
