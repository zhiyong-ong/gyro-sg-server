import sqlalchemy as db
from sqlalchemy.dialects.postgresql import ENUM

from app.db.base_class import Base
from app.core.constants import DrivingLicenceTypeEnum


class User(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    mobile_number = db.Column(db.Text, nullable=True)
    nric_number = db.Column(db.Text, nullable=True)
    driving_licence_type = db.Column(
        ENUM(
            DrivingLicenceTypeEnum,
            values_callable=lambda obj: [e.value for e in obj],
            name='drivinglicencetypeenum',
            nullable=True,
        )
    )
    is_superuser = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.id}>"
