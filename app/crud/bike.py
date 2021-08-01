from typing import Optional

from sqlalchemy.orm import Session, contains_eager, joinedload

from app.crud.base import CRUDBase
from app.models.bike import Bike, BikeModel
from app.schemas import BikeUpdate, BikeCreate


class CRUDBike(CRUDBase[Bike, BikeCreate, BikeUpdate]):
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
            query = query.filter(BikeModel.name == model)
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
        db_obj: Bike,
    ):
        delete_data = {"is_deleted": True}
        self.update(db, db_obj=db_obj, obj_in=delete_data)


bike = CRUDBike(Bike)
