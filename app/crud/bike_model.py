from typing import Optional, Union, List

from sqlalchemy.orm import Session

from app import models
from app.crud.base import CRUDBase
from app.schemas import BikeModelCreate, BikeModelUpdate


class CRUDBikeModel(CRUDBase[models.BikeModel, BikeModelCreate, BikeModelUpdate]):
    def filter_with_params(
        self,
        db: Session,
        *,
        is_deleted: Optional[bool] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        multi: Optional[bool] = True,
    ) -> Union[List[models.BikeModel], models.BikeModel]:
        query = db.query(self.model)
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
        db_obj: models.BikeModel,
    ):
        delete_data = {"is_deleted": True}
        self.update(db, db_obj=db_obj, obj_in=delete_data)


bike_model = CRUDBikeModel(models.BikeModel)
