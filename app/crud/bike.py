from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session, contains_eager, joinedload

from app import crud, models
from app.core.constants import TransmissionTypeEnum, DrivingLicenceTypeEnum
from app.crud.base import CRUDBase
from app.models import User
from app.schemas import BikeUpdate, BikeCreate, BikeCreateInput, BikeAvailabilityCreate


class CRUDBike(CRUDBase[models.Bike, BikeCreate, BikeUpdate]):
    def filter_with_params(
        self,
        db: Session,
        *,
        id: Optional[int] = None,
        model_name: Optional[List[str]] = None,
        transmission: Optional[List[str]] = None,
        licence_class: Optional[List[str]] = None,
        has_storage_rack: Optional[bool] = None,
        has_storage_box: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        multi: Optional[bool] = True,
    ):
        query = (
            db.query(self.model)
            .options(joinedload(self.model.model))
            .options(joinedload(self.model.user))
            .options(joinedload(self.model.transmission))
            .options(joinedload(self.model.licence_class))
            .options(joinedload(self.model.availabilities))
        )
        if model_name:
            query = query.join(self.model.model).filter(
                models.BikeModel.name.in_(model_name)
            )
        if transmission:
            query = query.join(self.model.transmission).filter(
                models.Transmission.name.in_(transmission)
            )
        if licence_class:
            query = query.join(self.model.licence_class).filter(
                models.LicenceClass.name.in_(licence_class)
            )
        if has_storage_rack:
            query = query.filter(self.model.storage_rack == True)
        if has_storage_box:
            query = query.filter(self.model.storage_box == True)
        if id:
            query = query.filter(self.model.id == id)
        if is_deleted is True:
            query = query.filter(self.model.is_deleted == True)
        if is_deleted is False:
            query = query.filter(self.model.is_deleted == False)
        if start_datetime and end_datetime:
            query = query.join(self.model.availabilities).filter(
                models.BikeAvailability.start_datetime <= start_datetime,
                models.BikeAvailability.end_datetime >= end_datetime
            )
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

    def create_bike(
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
            bike_availability_schema = BikeAvailabilityCreate(
                start_datetime=availability.start_datetime,
                end_datetime=availability.end_datetime,
                bike_id=bike_id,
            )
            crud.bike_availability.create(db, obj_in=bike_availability_schema)
        return bike


bike = CRUDBike(models.Bike)
