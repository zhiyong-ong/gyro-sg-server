from app import models
from app.crud.base import CRUDBase
from app.schemas import BikeAvailabilityCreate, BikeAvailabilityUpdate


class CRUDBikeAvailability(
    CRUDBase[models.BikeAvailability, BikeAvailabilityCreate, BikeAvailabilityUpdate]
):
    pass
    # def create(self, db: Session, *, obj_in: BikeAvailabilityCreate) -> BikeAvailability:


bike_availability = CRUDBikeAvailability(models.BikeAvailability)
