import logging
from typing import List, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, models
from app.api import deps
from app.core.constants import PUBLIC_DESC

router = APIRouter()
logger = logging.getLogger(__name__)
base_endpoint = ""
bike_endpoint = "/{bike_id}"
bike_user_endpoint = "/me"


@router.get(
    base_endpoint,
    response_model=List[schemas.BikeWithModel],
    description=PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bikes(
    *,
    db: Session = Depends(deps.get_db),
    model: str = None,
    offset: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve bikes.
    """
    logger.info(f"Retrieving all bikes based on query parameters")
    bikes = crud.bike.filter_with_params(db, model=model, offset=offset, limit=limit)
    return bikes


@router.get(
    bike_endpoint,
    response_model=schemas.BikeWithModel,
    description=PUBLIC_DESC,
    status_code=status.HTTP_200_OK,
)
def read_bike(*, db: Session = Depends(deps.get_db), bike_id: int):
    """
    Retrieve bike based on id
    """
    logger.info(f"Retrieving bike with id {bike_id}")
    bike = crud.bike.filter_with_params(db, id=bike_id, multi=False)
    return bike


@router.post(
    bike_user_endpoint,
    response_model=schemas.BikeWithModel,
    status_code=status.HTTP_201_CREATED,
)
def create_bike_for_user(
    *,
    db: Session = Depends(deps.get_db),
    bike_in: schemas.BikeCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new bike listing for current logged in user
    """
    logger.info(f"Creating bike {bike_in} for user: {current_user.id}")
    bike = crud.bike.create(db, obj_in=bike_in)
    return bike


# @router.patch(cur_user_endpoint, response_model=schemas.User)
# def update_current_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.UserUpdateCurrent,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update own user.
#     """
#     logger.info(f"Updating current user {user_in}")
#     user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
#     return user
#
#
# @router.patch(cur_user_password_endpoint, response_model=schemas.User)
# def update_current_user_password(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.UserUpdatePassword,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Update own user password.
#     """
#     logger.info(f"Updating current user password")
#     user = crud.user.update_password(db, db_obj=current_user, obj_in=user_in)
#     return user
#
#
# @router.patch(
#     user_endpoint, response_model=schemas.User, description=SUPERUSER_PRIVILEGE_DESC
# )
# def update_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_id: int,
#     user_in: schemas.UserUpdateInput,
#     current_user: models.User = Depends(deps.get_current_active_superuser),
# ) -> Any:
#     """
#     Update own user.
#     """
#     logger.info(f"Updating user id {user_id}")
#     user = crud.user.get(db, id=user_id)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this id does not exist in the system",
#         )
#     user = crud.user.update_with_superuser(db, db_obj=user, obj_in=user_in)
#     return user
