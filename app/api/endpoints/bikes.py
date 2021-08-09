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
bike_endpoint = "/{bike_id}"
bike_current_user_create_endpoint = "/me"
bike_current_user_endpoint = "/{bike_id}/me"


@router.get(
    base_endpoint,
    response_model=List[schemas.BikeWithRelationships],
    description="Get a list of all bikes. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bikes(
    *,
    db: Session = Depends(deps.get_db),
    model: str = None,
    is_deleted: Optional[bool] = None,
    offset: int = 0,
    limit: int = 100,
) -> Any:
    logger.info(f"Retrieving all bikes based on query parameters")
    bikes = crud.bike.filter_with_params(
        db, model=model, is_deleted=is_deleted, offset=offset, limit=limit
    )
    return bikes


@router.get(
    bike_endpoint,
    response_model=schemas.BikeWithRelationships,
    description="Get bike details based on bike id. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike(*, db: Session = Depends(deps.get_db), bike_id: int):
    logger.info(f"Retrieving bike with id {bike_id}")
    bike = crud.bike.filter_with_params(db, id=bike_id, multi=False)
    return bike


@router.post(
    bike_current_user_create_endpoint,
    response_model=schemas.BikeWithRelationships,
    status_code=status.HTTP_201_CREATED,
    description="Create bike for current user. " + BASIC_USER_DESC,
)
def create_bike_current_user(
    *,
    db: Session = Depends(deps.get_db),
    bike_in: schemas.BikeCreateInput,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    logger.info(f"Creating bike {bike_in} for user: {current_user.id}")
    bike = crud.bike.create(db, obj_in=bike_in, current_user=current_user)
    return bike


@router.patch(
    bike_current_user_endpoint,
    response_model=schemas.BikeWithRelationships,
    status_code=status.HTTP_200_OK,
    description="Update current user's bike based on the bike id. " + BASIC_USER_DESC,
)
def update_bike_current_user(
    *,
    db: Session = Depends(deps.get_db),
    bike_id: int,
    bike_in: schemas.BikeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    logger.info(f"Updating bike {bike_id} with {bike_in} for user: {current_user.id}")
    cur_bike = crud.bike.get(db, id=bike_id)
    if not cur_bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This bike with id {bike_id} cannot be found in the system.",
        )
    if cur_bike.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The bike with id {bike_id} does not belong to the current user.",
        )
    bike = crud.bike.update(db, db_obj=cur_bike, obj_in=bike_in)
    return bike


@router.patch(
    bike_endpoint,
    response_model=schemas.BikeWithRelationships,
    status_code=status.HTTP_200_OK,
    description="Update any bike based on the bike id. " + SUPERUSER_PRIVILEGE_DESC,
)
def update_bike(
    *,
    db: Session = Depends(deps.get_db),
    bike_id: int,
    bike_in: schemas.BikeUpdate,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    logger.info(f"Updating bike {bike_id} with {bike_in}")
    cur_bike = crud.bike.get(db, id=bike_id)
    if not cur_bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This bike with id {bike_id} cannot be found in the system.",
        )
    bike = crud.bike.update(db, db_obj=cur_bike, obj_in=bike_in)
    return bike


@router.delete(
    bike_current_user_endpoint,
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    description="Delete the current user's bike based on the bike id. "
    + BASIC_USER_DESC,
)
def delete_bike_current_user(
    *,
    db: Session = Depends(deps.get_db),
    bike_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    logger.info(f"Deleting bike {bike_id} for user: {current_user.id}")
    cur_bike = crud.bike.get(db, id=bike_id)
    if not cur_bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This bike with id {bike_id} cannot be found in the system.",
        )
    if cur_bike.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"The bike with id {bike_id} does not belong to the current user.",
        )
    crud.bike.delete(db, db_obj=cur_bike)
    return {"msg": "Bike deleted!"}


@router.delete(
    bike_endpoint,
    response_model=schemas.Msg,
    status_code=status.HTTP_200_OK,
    description="Delete any bike based on the bike id. " + SUPERUSER_PRIVILEGE_DESC,
)
def delete_bike(
    *,
    db: Session = Depends(deps.get_db),
    bike_id: int,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    logger.info(f"Deleting bike {bike_id}")
    cur_bike = crud.bike.get(db, id=bike_id)
    if not cur_bike:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"This bike with id {bike_id} cannot be found in the system.",
        )
    crud.bike.delete(db, db_obj=cur_bike)
    return {"msg": "Bike deleted!"}
