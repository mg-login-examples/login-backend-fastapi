from typing import List
from sqlalchemy.orm import Session

from data.schemas import items as itemsSchemas
from data.database.models.base import Base as BaseModel


def get_resource_item(db: Session, ResourceModel: BaseModel, item_id: int) -> BaseModel:
    return db.query(ResourceModel).filter(ResourceModel.id == item_id).first()

def get_resource_item_by_attribute(db: Session, ResourceModel: BaseModel, ResourceModel_attribute: any, attribute_value: any):
    return db.query(ResourceModel).filter(ResourceModel_attribute == attribute_value).first()

def get_resource_items(db: Session, ResourceModel: BaseModel, skip: int = 0, limit: int = 100) -> List[BaseModel]:
    return db.query(ResourceModel).offset(skip).limit(limit).all()

def create_resource_item(db: Session, item_to_create: BaseModel) -> BaseModel:
    db.add(item_to_create)
    db.commit()
    db.refresh(item_to_create)
    return item_to_create

def update_resource_item(db: Session, ResourceModel: BaseModel, item_dict: dict) -> BaseModel:
    db.query(ResourceModel).filter(ResourceModel.id == item_dict["id"]).update(item_dict)
    db.commit()
    db.flush()
    return db.query(ResourceModel).filter(ResourceModel.id == item_dict["id"]).first()

def delete_resource_item(db: Session, ResourceModel: BaseModel, item_id: int):
    db.query(ResourceModel).filter(ResourceModel.id == item_id).delete()
    db.commit()
