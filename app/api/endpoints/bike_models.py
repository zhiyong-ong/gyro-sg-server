import logging
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, models
from app.api import deps
from app.core.constants import PUBLIC_DESC, BASIC_USER_DESC, SUPERUSER_PRIVILEGE_DESC

router = APIRouter()
logger = logging.getLogger(__name__)
base_endpoint = ""
bike_model_endpoint = "/{bike_model_id}"


@router.get(
    base_endpoint,
    response_model=List[schemas.BikeModel],
    description="Get a list of all bike models. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike_models(
    *,
    db: Session = Depends(deps.get_db),
    is_deleted: Optional[bool] = None,
    offset: int = 0,
    limit: int = 100,
) -> Any:
    logger.info(f"Retrieving all bikes based on query parameters")
    bikes = crud.bike_model.filter_with_params(
        db, is_deleted=is_deleted, offset=offset, limit=limit
    )
    return bikes


@router.get(
    bike_model_endpoint,
    response_model=schemas.BikeModel,
    description="Get bike model details based on bike id. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike_model(*, db: Session = Depends(deps.get_db), bike_model_id: int):
    logger.info(f"Retrieving bike model with id {bike_model_id}")
    bike = crud.bike_model.get(db, id=bike_model_id)
    return bike


@router.post(
    base_endpoint,
    response_model=schemas.BikeModel,
    status_code=status.HTTP_201_CREATED,
    description="Create bike model. " + SUPERUSER_PRIVILEGE_DESC,
)
def create_bike_model(
    *,
    db: Session = Depends(deps.get_db),
    bike_model_in: schemas.BikeModelCreate,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    logger.info(f"Creating bike model {bike_model_in}")
    bike_model = crud.bike_model.create(db, obj_in=bike_model_in)
    return bike_model


@router.patch(
    bike_model_endpoint,
    response_model=schemas.BikeModel,
    status_code=status.HTTP_200_OK,
    description="Update bike model based on the bike model id. "
    + SUPERUSER_PRIVILEGE_DESC,
)
def update_bike_model(
    *,
    db: Session = Depends(deps.get_db),
    bike_model_id: int,
    bike_model_in: schemas.BikeModelUpdate,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    logger.info(f"Updating bike model {bike_model_id} with {bike_model_id}.")
    cur_bike_model = crud.bike_model.get(db, id=bike_model_id)
    if not cur_bike_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The bike model with id {bike_model_id} cannot be found in the system.",
        )
    bike_model = crud.bike_model.update(db, db_obj=cur_bike_model, obj_in=bike_model_in)
    return bike_model


@router.delete(
    bike_model_endpoint,
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    description="Delete bike model based on the bike model id. "
    + SUPERUSER_PRIVILEGE_DESC,
)
def delete_bike_model(
    *,
    db: Session = Depends(deps.get_db),
    bike_model_id: int,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    logger.info(f"Deleting bike model {bike_model_id}")
    cur_bike_model = crud.bike_model.get(db, id=bike_model_id)
    if not cur_bike_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The bike model with id {bike_model_id} cannot be found in the system.",
        )
    crud.bike_model.delete(db, db_obj=cur_bike_model)
    return {"msg": "Bike model deleted!"}
