import logging
from datetime import datetime
from typing import List, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, models
from app.api import deps
from app.core.constants import (
    PUBLIC_DESC,
    BASIC_USER_DESC,
    SUPERUSER_PRIVILEGE_DESC,
)

router = APIRouter()
logger = logging.getLogger(__name__)
base_endpoint = ""
filter_params_endpoint = "/filter-params"
bike_endpoint = "/{bike_id}"
bike_current_user_create_endpoint = "/me"
bike_current_user_endpoint = "/{bike_id}/me"


@router.get(
    filter_params_endpoint,
    response_model=schemas.BikeFilterParams,
    description="Get bike filter params. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike_filter_params_endpoint(*, db: Session = Depends(deps.get_db)):
    logger.info(f"Retrieving bike filter params")
    response = {
        "licence_class": {
            "header": "Licence Class",
            "fields": crud.licence_class.get_multi(db, offset=None, limit=None),
        },
        "transmission": {
            "header": "Transmission",
            "fields": crud.transmission.get_multi(db, offset=None, limit=None),
        },
        "other": {
            "header": "Others",
            "fields": [
                {
                    "name": "has_storage_rack",
                    "description": "Includes storage rack",
                },
                {
                    "name": "has_storage_box",
                    "description": "Includes storage box",
                },
            ],
        },
    }
    return response


@router.get(
    base_endpoint,
    response_model=List[schemas.BikeResponse],
    description="Get a list of all bikes. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bikes(
    *,
    db: Session = Depends(deps.get_db),
    model_name: Optional[List[str]] = Query(None),
    transmission: Optional[List[str]] = Query(None),
    licence_class: Optional[List[str]] = Query(None),
    has_storage_rack: Optional[bool] = None,
    has_storage_box: Optional[bool] = None,
    is_deleted: Optional[bool] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    offset: int = 0,
    limit: int = 100,
) -> Any:
    if start_datetime and not end_datetime or end_datetime and not start_datetime:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="If start_datetime is provided, end_datetime has to be provided as well."
        )
    if start_datetime.tzinfo is None or start_datetime.tzinfo.utcoffset(start_datetime) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="start_datetime has to be timezone aware."
        )
    if end_datetime.tzinfo is None or end_datetime.tzinfo.utcoffset(end_datetime) is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_datetime has to be timezone aware."
        )
    if start_datetime and end_datetime:
        if start_datetime > end_datetime:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="end_datetime has to be set further in time than start_datetime."
            )
    logger.info(f"Retrieving all bikes based on query parameters")
    bikes = crud.bike.filter_with_params(
        db,
        model_name=model_name,
        transmission=transmission,
        licence_class=licence_class,
        has_storage_rack=has_storage_rack,
        has_storage_box=has_storage_box,
        is_deleted=is_deleted,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        offset=offset,
        limit=limit,
    )
    return bikes


@router.get(
    bike_endpoint,
    response_model=schemas.BikeResponse,
    description="Get bike details based on bike id. " + PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike(*, db: Session = Depends(deps.get_db), bike_id: int):
    logger.info(f"Retrieving bike with id {bike_id}")
    bike = crud.bike.filter_with_params(db, id=bike_id, multi=False)
    return bike


@router.post(
    bike_current_user_create_endpoint,
    response_model=schemas.BikeResponse,
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
    bike = crud.bike.create_bike(db, obj_in=bike_in, current_user=current_user)
    return bike


@router.patch(
    bike_current_user_endpoint,
    response_model=schemas.BikeResponse,
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
    response_model=schemas.BikeResponse,
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
