from app import models
from app.crud.base import CRUDBase
from app.schemas import TransmissionCreate, TransmissionUpdate


class CRUDTransmission(CRUDBase[models.Transmission, TransmissionCreate, TransmissionUpdate]):
    pass

transmission = CRUDTransmission(models.Transmission)
