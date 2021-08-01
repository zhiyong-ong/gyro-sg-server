from __future__ import annotations

from typing import Optional, List

from pydantic.main import BaseModel

from app.core.constants import DrivingLicenceTypeEnum


class BikeBase(BaseModel):
    color: Optional[str] = None
    required_licence: Optional[DrivingLicenceTypeEnum] = None
    transmission: Optional[str] = None
    storage_box: Optional[str] = None
    rate: Optional[str] = None
    rate_unit: Optional[str] = None
    description: Optional[str] = None
    images: Optional[List[str]] = None
    model_id: Optional[int] = None


class BikeCreate(BikeBase):
    model_id: int


class BikeUpdate(BikeBase):
    pass


class Bike(BikeBase):
    id: int

    class Config:
        orm_mode = True


class BikeWithModel(BikeBase):
    id: int
    model: "BikeModel"

    class Config:
        orm_mode = True


class BikeModelBase(BaseModel):
    name: Optional[str]


class BikeModelCreate(BikeModelBase):
    name: str


class BikeModelUpdate(BikeModelBase):
    name: str


class BikeModel(BikeModelBase):
    id: int
    name: str

    class Config:
        orm_mode = True


BikeWithModel.update_forward_refs()
