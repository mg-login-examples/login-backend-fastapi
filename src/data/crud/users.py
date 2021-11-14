from sqlalchemy.orm import Session

from data.schemas import users as userSchemas
from data.database.models.user import User as UserModel
from data.crud import base as baseCrud

def get_user(db: Session, user_id: int) -> UserModel:
    return baseCrud.get_resource_item(db, UserModel, user_id)

def get_user_by_email(db: Session, email: str):
    return baseCrud.get_resource_item_by_attribute(db, UserModel, UserModel.email, email)

def create_user(db: Session, user: userSchemas.UserCreate) -> UserModel:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
    return baseCrud.create_resource_item(db, db_user)
