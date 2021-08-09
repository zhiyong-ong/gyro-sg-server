from typing import Optional

from sqlalchemy.orm import Session, contains_eager, joinedload

from app import crud, models
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import BikeUpdate, BikeCreate, BikeCreateInput, BikeAvailabilityCreate


class CRUDBike(CRUDBase[models.Bike, BikeCreate, BikeUpdate]):
    def filter_with_params(
        self,
        db: Session,
        *,
        id: Optional[int] = None,
        model: Optional[str] = None,
        is_deleted: Optional[bool] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        multi: Optional[bool] = True,
    ):
        query = (
            db.query(self.model)
            .join(self.model.model)
            .options(contains_eager(self.model.model))
            .options(joinedload(self.model.user))
        )
        if model:
            query = query.filter(models.BikeModel.name == model)
        if id:
            query = query.filter(self.model.id == id)
        if is_deleted is True:
            query = query.filter(self.model.is_deleted == True)
        if is_deleted is False:
            query = query.filter(self.model.is_deleted == False)

        query = query.offset(offset).limit(limit)
        if multi:
            return query.all()
        else:
            return query.first()

    def delete(
        self,
        db: Session,
        *,
        db_obj: models.Bike,
    ):
        delete_data = {"is_deleted": True}
        self.update(db, db_obj=db_obj, obj_in=delete_data)

    def create(
        self, db: Session, *, obj_in: BikeCreateInput, current_user: User
    ) -> models.Bike:
        availability_list = (
            obj_in.availabilities if obj_in.availabilities is not None else []
        )
        del obj_in.availabilities

        bike_create_schema = BikeCreate(**obj_in.dict(), user_id=current_user.id)
        bike = super().create(db, obj_in=bike_create_schema)
        bike_id = bike.id

        for availability in availability_list:
            print(availability.start_datetime)
            bike_availability_schema = BikeAvailabilityCreate(
                start_datetime=availability.start_datetime,
                end_datetime=availability.end_datetime,
                bike_id=bike_id,
            )
            crud.bike_availability.create(db, obj_in=bike_availability_schema)
        return bike


bike = CRUDBike(models.Bike)
