from typing import List

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from .sqlalchemy_base_model import Base as BaseModel

def get_resource_items_count(db: Session, ResourceModel) -> int:
    return db.query(ResourceModel).count()

def get_resource_item(db: Session, ResourceModel, item_id: int) -> BaseModel:
    return db.query(ResourceModel).filter(ResourceModel.id == item_id).first()

def get_resource_item_by_attribute(db: Session, ResourceModel, ResourceModel_attribute: any, attribute_value: any):
    return db.query(ResourceModel).filter(ResourceModel_attribute == attribute_value).first()

def get_resource_items(db: Session, ResourceModel, skip: int = 0, limit: int = 100) -> List[BaseModel]:
    return db.query(ResourceModel).offset(skip).limit(limit).all()

def create_resource_item(db: Session, ResourceModel, item_to_create: BaseSchema) -> BaseModel:
    db_item = ResourceModel(**item_to_create.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_resource_item_partial(db: Session, ResourceModel, item_to_update: BaseSchema) -> BaseModel:
    db_item = db.query(ResourceModel).filter(ResourceModel.id == item_to_update.id).one_or_none()
    if db_item is None:
        return None
    for item_field, field_value in vars(item_to_update).items():
        if (type(field_value) is not list):
            setattr(db_item, item_field, field_value) if field_value else None
        else:
            RelatedItemModel = getattr(ResourceModel, item_field).property.mapper.class_
            setattr(db_item, item_field, [])
            related_items = field_value
            for related_item in related_items:
                db_related_item = db.query(RelatedItemModel).filter(RelatedItemModel.id == related_item.id).first()
                added_related_items = getattr(db_item, item_field)
                added_related_items.append(db_related_item)
                setattr(db_item, item_field, added_related_items)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_resource_item_full(db: Session, ResourceModel, item_to_update: BaseSchema) -> BaseModel:
    db_item = db.query(ResourceModel).filter(ResourceModel.id == item_to_update.id).one_or_none()
    if db_item is None:
        return None
    for item_field, field_value in vars(item_to_update).items():
        if (type(field_value) is not list):
            setattr(db_item, item_field, field_value)
        else:
            RelatedItemModel = getattr(ResourceModel, item_field).property.mapper.class_
            setattr(db_item, item_field, [])
            related_items = field_value
            for related_item in related_items:
                db_related_item = db.query(RelatedItemModel).filter(RelatedItemModel.id == related_item.id).first()
                added_related_items = getattr(db_item, item_field)
                added_related_items.append(db_related_item)
                setattr(db_item, item_field, added_related_items)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_resource_item(db: Session, ResourceModel: BaseModel, item_id: int):
    db.query(ResourceModel).filter(ResourceModel.id == item_id).delete()
    db.commit()
