from app.crud.base import CRUDBase
from app.models.bike import BikeModel
from app.schemas import BikeModelCreate, BikeModelUpdate


class CRUDBikeModel(CRUDBase[BikeModel, BikeModelCreate, BikeModelUpdate]):
    pass


bike_model = CRUDBikeModel(BikeModel)
