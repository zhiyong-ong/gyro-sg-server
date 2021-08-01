import logging
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, models
from app.api import deps
from app.core.constants import SUPERUSER_PRIVILEGE_DESC, BASIC_USER_DESC, PUBLIC_DESC

router = APIRouter()
logger = logging.getLogger(__name__)
base_endpoint = ""
user_endpoint = "/{user_id}"
cur_user_endpoint = "/me"
cur_user_password_endpoint = "/me/password"
open_endpoint = "/open"


@router.get(
    base_endpoint,
    response_model=List[schemas.UserWithId],
    description=SUPERUSER_PRIVILEGE_DESC,
    status_code=status.HTTP_200_OK,
)
def read_users(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    offset: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    logger.info(f"Retrieving all users")
    users = crud.user.get_multi(db, offset=offset, limit=limit)
    return users


@router.get(
    cur_user_endpoint,
    response_model=schemas.User,
    description=BASIC_USER_DESC,
    status_code=status.HTTP_200_OK,
)
def read_current_user(
    *, current_user: models.User = Depends(deps.get_current_active_user)
):
    logger.info(f"Retrieving current user {current_user.email}")
    return current_user


@router.get(
    user_endpoint,
    response_model=schemas.UserWithId,
    description=SUPERUSER_PRIVILEGE_DESC,
    status_code=status.HTTP_200_OK,
)
def read_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
    user_id: int,
) -> Any:
    """
    Retrieve users.
    """
    logger.info(f"Retrieving user id {user_id}")
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    return user


@router.post(
    open_endpoint,
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    description=PUBLIC_DESC,
)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    logger.info(f"Creating user {user_in.email}")
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post(
    base_endpoint,
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    description=SUPERUSER_PRIVILEGE_DESC,
)
def create_user_superuser(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreateSuperuser,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user using superuse
    """
    logger.info(f"Creating user {user_in.email}")
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create_superuser(db, obj_in=user_in)
    return user


@router.patch(
    cur_user_endpoint, response_model=schemas.User, description=BASIC_USER_DESC
)
def update_current_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdateCurrent,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    logger.info(f"Updating current user {user_in}")
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.patch(
    cur_user_password_endpoint, response_model=schemas.User, description=BASIC_USER_DESC
)
def update_current_user_password(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdatePassword,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user password.
    """
    logger.info(f"Updating current user password")
    user = crud.user.update_password(db, db_obj=current_user, obj_in=user_in)
    return user


@router.patch(
    user_endpoint, response_model=schemas.User, description=SUPERUSER_PRIVILEGE_DESC
)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdateInput,
    current_superuser: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update own user.
    """
    logger.info(f"Updating user id {user_id}")
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = crud.user.update_with_superuser(db, db_obj=user, obj_in=user_in)
    return user
