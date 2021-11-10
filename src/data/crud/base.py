from typing import List
from sqlalchemy.orm import Session

from data.schemas import items as itemsSchemas
from data.database.models.base import Base as BaseModel


def get_object(db: Session, object_model: BaseModel, object_id: int) -> BaseModel:
    return db.query(object_model).filter(object_model.id == object_id).first()

def get_all_objects(db: Session, object_model: BaseModel, skip: int = 0, limit: int = 100) -> List[BaseModel]:
    return db.query(object_model).offset(skip).limit(limit).all()

def create_object(db: Session, object_to_create: BaseModel) -> BaseModel:
    db.add(object_to_create)
    db.commit()
    db.refresh(object_to_create)
    return object_to_create

def delete_object(db: Session, object_model: BaseModel, object_id: int):
    db.query(object_model).filter(object_model.id == object_id).delete()
    db.commit()
