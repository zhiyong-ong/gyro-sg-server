import sqlalchemy as db
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = db.Column(db.BigInteger, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    mobile_number = db.Column(db.Text, nullable=True)
    nric_number = db.Column(db.Text, nullable=True)
    is_superuser = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    bikes = relationship("Bike", back_populates="user")
    licence_class_id = db.Column(db.Integer, db.ForeignKey("licence_class.id"))
    licence_class = relationship("LicenceClass")

    def __repr__(self):
        return f"<User {self.id}>"
