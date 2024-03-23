from typing import Tuple, Any

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

def get_resource_items_count(db: Session, ResourceModel) -> int:
    return db.query(ResourceModel).count()

def get_resource_item(db: Session, ResourceModel, item_id: int) -> Any:
    return db.query(ResourceModel).filter(ResourceModel.id == item_id).first()

def get_resource_item_by_attribute(db: Session, ResourceModel, ResourceModel_attribute: any, attribute_value: any) -> Any:
    return db.query(ResourceModel).filter(ResourceModel_attribute == attribute_value).first()

def get_resource_items_by_attribute_filtered(db: Session, ResourceModel, ResourceModel_attribute: any, attribute_filter: any, skip: int = 0, limit: int = 100) -> list[Any]:
    return db.query(ResourceModel).filter(ResourceModel_attribute.like(attribute_filter)).offset(skip).limit(limit).all()

def get_resource_items_filtered_by_like_multiple_attributes_count(db: Session, ResourceModel, ResourceModel_attributes: any, attribute_filters: any) -> int:
    return db.query(ResourceModel).filter(
        *[ResourceModel_attribute.like(attribute_filter) for (ResourceModel_attribute, attribute_filter) in zip(ResourceModel_attributes, attribute_filters)]
    ).count()

def get_resource_items_filtered_by_like_multiple_attributes(db: Session, ResourceModel, ResourceModel_attributes: any, attribute_filters: any, skip: int = 0, limit: int = 100) -> list[Any]:
    return db.query(ResourceModel).filter(
        *[ResourceModel_attribute.like(attribute_filter) for (ResourceModel_attribute, attribute_filter) in zip(ResourceModel_attributes, attribute_filters)]
    ).offset(skip).limit(limit).all()

def get_resource_items_by_attribute_in_list(db: Session, ResourceModel, ResourceModel_attribute: any, attribute_in_list: list[any], all = False, skip: int = 0, limit: int = 100) -> list[Any]:
    query = db.query(ResourceModel).filter(ResourceModel_attribute.in_(attribute_in_list))
    if all:
        return query.all()
    else:
        return query.offset(skip).limit(limit).all()

def get_resource_item_by_attributes(db: Session, ResourceModel, ResourceModel_attributes_and_values: list[Tuple]) -> Any:
    query = db.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    return query.first()

def get_resource_items(db: Session, ResourceModel, skip: int = 0, limit: int = 100) -> list[Any]:
    return db.query(ResourceModel).offset(skip).limit(limit).all()

def get_resource_items_by_attribute(db: Session, ResourceModel, ResourceModel_attribute: any, attribute_value: any, skip: int = 0, limit: int = 100) -> list[Any]:
    return db.query(ResourceModel).filter(ResourceModel_attribute == attribute_value).offset(skip).limit(limit).all()

def get_resource_items_by_attributes(db: Session, ResourceModel, ResourceModel_attributes_and_values: list[Tuple], skip: int = 0, limit: int = 100) -> Any:
    query = db.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    return query.offset(skip).limit(limit).all()

def create_resource_item(db: Session, ResourceModel, item_to_create: BaseSchema) -> Any:
    db_item = ResourceModel(**item_to_create.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_resource_item_partial(db: Session, ResourceModel, item_to_update: BaseSchema) -> Any:
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

def update_resource_item_full(db: Session, ResourceModel, item_to_update: BaseSchema) -> Any:
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

def delete_resource_item(db: Session, ResourceModel: Any, item_id: int):
    db.query(ResourceModel).filter(ResourceModel.id == item_id).delete()
    db.commit()

def delete_resource_item_by_attribute(db: Session, ResourceModel: Any, ResourceModel_attribute: any, attribute_value: any):
    db_item = db.query(ResourceModel).filter(ResourceModel_attribute == attribute_value).first()
    if db_item:
        db.delete(db_item)
        db.commit()

def delete_resource_item_by_attributes(db: Session, ResourceModel: Any, ResourceModel_attributes_and_values: list[Tuple]):
    query = db.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    db_item = query.first()
    if db_item:
        db.delete(db_item)
        db.commit()
