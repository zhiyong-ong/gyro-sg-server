import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Bike(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    color = db.Column(db.Text)
    storage_rack = db.Column(db.Boolean)
    storage_box = db.Column(db.Boolean)
    location = db.Column(db.Text)
    rate = db.Column(db.Float)
    rate_unit = db.Column(db.Text)
    description = db.Column(db.Text)
    images = db.Column(db.ARRAY(db.Text))
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    licence_class_id = db.Column(db.Integer, db.ForeignKey("licence_class.id"))
    licence_class = relationship("LicenceClass")

    transmission_id = db.Column(db.Integer, db.ForeignKey("transmission.id"))
    transmission = relationship("Transmission")

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


class Transmission(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Transmission {self.id}>"


class LicenceClass(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<LicenceClass {self.id}>"
