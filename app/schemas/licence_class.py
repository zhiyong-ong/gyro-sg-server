from __future__ import annotations
from typing import Optional

from pydantic.main import BaseModel


class LicenceClassBase(BaseModel):
    name: Optional[str]
    description: Optional[str]


class LicenceClassCreate(LicenceClassBase):
    name: str


class LicenceClassUpdate(LicenceClassBase):
    pass


class LicenceClass(LicenceClassBase):
    name: str

    class Config:
        orm_mode = True
