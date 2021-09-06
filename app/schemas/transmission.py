from __future__ import annotations
from typing import Optional

from pydantic.main import BaseModel


class TransmissionBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class TransmissionCreate(TransmissionBase):
    name: str


class TransmissionUpdate(TransmissionBase):
    pass


class Transmission(TransmissionBase):
    name: str

    class Config:
        orm_mode = True
