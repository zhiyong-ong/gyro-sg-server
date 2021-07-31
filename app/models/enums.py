from app.core.constants import DrivingLicenceTypeEnum
import sqlalchemy as db

driving_licence_type_enum = db.Enum(
	DrivingLicenceTypeEnum,
	values_callable=lambda obj: [e.value for e in obj],
	nullable=True,
)