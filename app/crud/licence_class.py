from app import models
from app.crud.base import CRUDBase
from app.schemas import LicenceClassUpdate, LicenceClassCreate


class CRUDLicenceClass(CRUDBase[models.LicenceClass, LicenceClassCreate, LicenceClassUpdate]):
    pass

licence_class = CRUDLicenceClass(models.LicenceClass)
