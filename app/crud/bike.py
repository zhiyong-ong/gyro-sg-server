from typing import Optional

from sqlalchemy.orm import Session, contains_eager

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
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        multi: Optional[bool] = True,
    ):
        query = (
            db.query(self.model)
            .join(self.model.model)
            .options(contains_eager(self.model.model))
        )
        if model:
            query = query.filter(BikeModel.name == model)
        if id:
            query = query.filter(self.model.id == id)
        query = query.offset(offset).limit(limit)
        if multi:
            return query.all()
        else:
            return query.first()


bike = CRUDBike(Bike)
