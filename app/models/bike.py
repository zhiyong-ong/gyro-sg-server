import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.core.constants import DrivingLicenceTypeEnum, TransmissionTypeEnum
from sqlalchemy.dialects.postgresql import ENUM


class Bike(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    color = db.Column(db.Text)
    required_licence = db.Column(
        ENUM(
            DrivingLicenceTypeEnum,
            values_callable=lambda obj: [e.value for e in obj],
            nullable=True,
            name="drivinglicencetypeenum",
            create_type=False,
        )
    )
    transmission = db.Column(
        ENUM(
            TransmissionTypeEnum,
            values_callable=lambda obj: [e.value for e in obj],
            nullable=True,
            name="transmissiontypeenum",
        )
    )
    storage_box = db.Column(db.Boolean)
    location = db.Column(db.Text)
    rate = db.Column(db.Float)
    rate_unit = db.Column(db.Text)
    description = db.Column(db.Text)
    images = db.Column(db.ARRAY(db.Text))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    model_id = db.Column(
        db.BigInteger, db.ForeignKey("bike_model.id"), index=True, nullable=False
    )
    model = relationship("BikeModel", back_populates="bikes")

    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"))
    user = relationship("User", back_populates="bikes")

    availabilities = relationship("BikeAvailability", back_populates="bike")

    def __repr__(self):
        return f"<Bike {self.id}>"


class BikeModel(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    bikes = relationship("Bike", back_populates="model")

    __table_args__ = (
        db.Index(
            "ix_unique_name_bike_model",
            "name",
            unique=True,
            postgresql_where=(~is_deleted),
        ),
    )

    def __repr__(self):
        return f"<BikeModel {self.id}>"


class BikeAvailability(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    start_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    end_datetime = db.Column(db.DateTime(timezone=True), nullable=False)
    bike_id = db.Column(db.BigInteger, db.ForeignKey("bike.id"))
    bike = relationship("Bike", back_populates="availabilities")

    def __repr__(self):
        return f"<BikeAvailability {self.id}>"
