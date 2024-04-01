from typing import Tuple, Any, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel as BaseSchema


def get_resource_items_count(
    sql_db_session: Session, ResourceModel: DeclarativeMeta
) -> int:
    return sql_db_session.query(ResourceModel).count()


def get_resource_item(
    sql_db_session: Session, ResourceModel: Type[DeclarativeMeta], item_id: int
) -> Any:
    if not hasattr(ResourceModel, "id"):
        raise Exception("Model does not have id field")
    return (
        sql_db_session.query(ResourceModel).filter(ResourceModel.id == item_id).first()
    )


def get_resource_item_by_attribute(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attribute: Any,
    attribute_value: Any,
) -> Any:
    return (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel_attribute == attribute_value)
        .first()
    )


def get_resource_items_by_attribute_filtered(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attribute: Any,
    attribute_filter: Any,
    skip: int = 0,
    limit: int = 100,
) -> list[Any]:
    return (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel_attribute.like(attribute_filter))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_resource_items_filtered_by_like_multiple_attributes_count(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attributes: Any,
    attribute_filters: Any,
) -> int:
    return (
        sql_db_session.query(ResourceModel)
        .filter(
            *[
                ResourceModel_attribute.like(attribute_filter)
                for (ResourceModel_attribute, attribute_filter) in zip(
                    ResourceModel_attributes, attribute_filters
                )
            ]
        )
        .count()
    )


def get_resource_items_filtered_by_like_multiple_attributes(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attributes: Any,
    attribute_filters: Any,
    skip: int = 0,
    limit: int = 100,
) -> list[Any]:
    return (
        sql_db_session.query(ResourceModel)
        .filter(
            *[
                ResourceModel_attribute.like(attribute_filter)
                for (ResourceModel_attribute, attribute_filter) in zip(
                    ResourceModel_attributes, attribute_filters
                )
            ]
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_resource_items_by_attribute_in_list(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attribute: Any,
    attribute_in_list: list[Any],
    all=False,
    skip: int = 0,
    limit: int = 100,
) -> list[Any]:
    query = sql_db_session.query(ResourceModel).filter(
        ResourceModel_attribute.in_(attribute_in_list)
    )
    if all:
        return query.all()
    else:
        return query.offset(skip).limit(limit).all()


def get_resource_item_by_attributes(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attributes_and_values: list[Tuple],
) -> Any:
    query = sql_db_session.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    return query.first()


def get_resource_items(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    skip: int = 0,
    limit: int = 100,
) -> list[Any]:
    return sql_db_session.query(ResourceModel).offset(skip).limit(limit).all()


def get_resource_items_by_attribute(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attribute: Any,
    attribute_value: Any,
    skip: int = 0,
    limit: int = 100,
) -> list[Any]:
    return (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel_attribute == attribute_value)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_resource_items_by_attributes(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attributes_and_values: list[Tuple],
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = sql_db_session.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    return query.offset(skip).limit(limit).all()


def create_resource_item(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    item_to_create: BaseSchema,
) -> Any:
    db_item = ResourceModel(**item_to_create.model_dump())
    sql_db_session.add(db_item)
    sql_db_session.commit()
    sql_db_session.refresh(db_item)
    return db_item


def update_resource_item_partial(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    item_to_update: BaseSchema,
) -> Any:
    if not hasattr(ResourceModel, "id") or not hasattr(item_to_update, "id"):
        raise Exception("Model does not have id field")
    db_item = (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel.id == item_to_update.id)
        .one_or_none()
    )
    if db_item is None:
        return None
    for item_field, field_value in vars(item_to_update).items():
        if type(field_value) is not list:
            setattr(db_item, item_field, field_value)
        else:
            RelatedItemModel = getattr(ResourceModel, item_field).property.mapper.class_
            setattr(db_item, item_field, [])
            related_items = field_value
            for related_item in related_items:
                db_related_item = (
                    sql_db_session.query(RelatedItemModel)
                    .filter(RelatedItemModel.id == related_item.id)
                    .first()
                )
                added_related_items = getattr(db_item, item_field)
                added_related_items.append(db_related_item)
                setattr(db_item, item_field, added_related_items)
    sql_db_session.add(db_item)
    sql_db_session.commit()
    sql_db_session.refresh(db_item)
    return db_item


def update_resource_item_full(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    item_to_update: BaseSchema,
) -> Any:
    if not hasattr(ResourceModel, "id") or not hasattr(item_to_update, "id"):
        raise Exception("Model does not have id field")
    db_item = (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel.id == item_to_update.id)
        .one_or_none()
    )
    if db_item is None:
        return None
    for item_field, field_value in vars(item_to_update).items():
        if type(field_value) is not list:
            setattr(db_item, item_field, field_value)
        else:
            RelatedItemModel = getattr(ResourceModel, item_field).property.mapper.class_
            setattr(db_item, item_field, [])
            related_items = field_value
            for related_item in related_items:
                db_related_item = (
                    sql_db_session.query(RelatedItemModel)
                    .filter(RelatedItemModel.id == related_item.id)
                    .first()
                )
                added_related_items = getattr(db_item, item_field)
                added_related_items.append(db_related_item)
                setattr(db_item, item_field, added_related_items)
    sql_db_session.add(db_item)
    sql_db_session.commit()
    sql_db_session.refresh(db_item)
    return db_item


def delete_resource_item(
    sql_db_session: Session, ResourceModel: Type[DeclarativeMeta], item_id: int
):
    if not hasattr(ResourceModel, "id"):
        raise Exception("Model does not have id field")
    sql_db_session.query(ResourceModel).filter(ResourceModel.id == item_id).delete()
    sql_db_session.commit()


def delete_resource_item_by_attribute(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attribute: Any,
    attribute_value: Any,
):
    db_item = (
        sql_db_session.query(ResourceModel)
        .filter(ResourceModel_attribute == attribute_value)
        .first()
    )
    if db_item:
        sql_db_session.delete(db_item)
        sql_db_session.commit()


def delete_resource_item_by_attributes(
    sql_db_session: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceModel_attributes_and_values: list[Tuple],
):
    query = sql_db_session.query(ResourceModel)
    for attribute_and_value in ResourceModel_attributes_and_values:
        query = query.filter(attribute_and_value[0] == attribute_and_value[1])
    db_item = query.first()
    if db_item:
        sql_db_session.delete(db_item)
        sql_db_session.commit()
