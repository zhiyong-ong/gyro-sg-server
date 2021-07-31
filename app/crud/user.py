from typing import Optional, Dict, Any, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import UserCreate, UserUpdate, UserUpdateCurrent, UserUpdatePassword


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
	def get_by_email(self, db: Session, *, email: str):
		return db.query(User).filter(User.email == email).first()

	def create(self, db: Session, *, obj_in: UserCreate) -> User:
		db_obj = User(
			email=obj_in.email,
			password_hash=get_password_hash(obj_in.password),
			first_name=obj_in.first_name,
			last_name=obj_in.last_name,
			mobile_number=obj_in.mobile_number,
			nric_number=obj_in.nric_number,
			driving_licence_type=obj_in.driving_licence_type
		)
		return self.create_db_model(db, db_model_in=db_obj)

	def update_with_superuser(
		self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
	) -> User:
		if isinstance(obj_in, dict):
			update_data = obj_in
		else:
			update_data = obj_in.dict(exclude_unset=True)
		if update_data["password"]:
			password_hash = get_password_hash(update_data["password"])
			del update_data["password"]
			update_data["password_hash"] = password_hash
		return super().update(db, db_obj=db_obj, obj_in=update_data)


	def update_password(
		self, db: Session, *, db_obj: User, obj_in: Union[UserUpdatePassword]
	) -> User:
		if not verify_password(obj_in.cur_password, db_obj.password_hash):
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Incorrect current password given."
			)
		new_password_hash = get_password_hash(obj_in.new_password)
		update_data = UserUpdate(password_hash=new_password_hash)
		return super().update(db, db_obj=db_obj, obj_in=update_data)

	def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
		user = self.get_by_email(db, email=email)
		if not user:
			return None
		if not verify_password(password, user.password_hash):
			return None
		return user

	def is_active(self, user: User) -> bool:
		return user.is_active

	def is_superuser(self, user: User) -> bool:
		return user.is_superuser

	def is_active_superuser(self, user: User) -> bool:
		return user.is_active and user.is_superuser


user = CRUDUser(User)
