import sqlalchemy as db
from app.db.base_class import Base
from app.core.constants import DrivingLicenceTypeEnum
from sqlalchemy.dialects.postgresql import ENUM


class Bike(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    model = db.Column(db.Integer)
    color = db.Column(db.Text)
    required_licence = db.Column(
        ENUM(
            DrivingLicenceTypeEnum,
            values_callable=lambda obj: [e.value for e in obj],
            nullable=True,
            name='drivinglicencetypeenum',
        )
    )
    transmission = db.Column(db.Text)
    storage_box = db.Column(db.Boolean)
    location = db.Column(db.Text)
    rate = db.Column(db.Integer)
    rate_unit = db.Column(db.Text)
    description = db.Column(db.Text)
    images = db.Column(db.ARRAY(db.Text))

    def __repr__(self):
        return f"<Bike {self.id}>"
