from typing import Any, Type

from bson import ObjectId
from pydantic import BaseModel
from pymongo.database import Database


def get_resource_items_count(
    mongo_db: Database,
    db_table: str,
    filter: dict[str, Any] = {},
) -> int:
    items_count = mongo_db[db_table].count_documents(filter)
    return items_count


def get_resource_items(
    mongo_db: Database,
    db_table: str,
    filter: dict[str, Any] = {},
    limit=0,
    skip=0,
):
    items_db = mongo_db[db_table].find(filter, limit=limit, skip=skip)
    return items_db


def get_resource_items_pydantized(
    mongo_db: Database,
    db_table: str,
    ItemSchema: Type[BaseModel],
    filter: dict[str, Any] = {},
    limit=0,
    skip=0,
):
    items_db = get_resource_items(
        mongo_db, db_table, filter=filter, limit=limit, skip=skip
    )
    items: list[BaseModel] = []
    for item_db in items_db:
        items.append(ItemSchema(**item_db))
    return items


def get_resource_item_by_filter(
    mongo_db: Database,
    db_table: str,
    filter: dict[str, Any] = {},
) -> dict | None:
    item_db = mongo_db[db_table].find_one(filter)
    return item_db


def get_resource_item_by_id(
    mongo_db: Database,
    db_table: str,
    item_id: str,
) -> dict | None:
    id_filter = {"_id": ObjectId(item_id)}
    item_db = mongo_db[db_table].find_one(id_filter)
    return item_db


def create_resource_item(
    mongo_db: Database,
    db_table: str,
    item_to_create: dict | BaseModel,
) -> dict[str, Any]:
    item_dict: dict[str, Any] = (
        item_to_create.model_dump()
        if isinstance(item_to_create, BaseModel)
        else item_to_create
    )
    result = mongo_db[db_table].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict


def update_item_by_id(
    mongo_db: Database,
    db_table: str,
    item_id: str,
    item_fields_to_update: dict | BaseModel,
):
    id_filter = {"_id": ObjectId(item_id)}
    item_fields_to_update = (
        item_fields_to_update.model_dump()
        if isinstance(item_fields_to_update, BaseModel)
        else item_fields_to_update
    )
    mongo_db[db_table].update_one(id_filter, {"$set": item_fields_to_update})
    return


def update_item_by_filter(
    mongo_db: Database,
    db_table: str,
    filter: dict,
    item_fields_to_update: dict | BaseModel,
):
    mongo_db[db_table].update_one(filter, {"$set": item_fields_to_update})
    return


def delete_resource_item_by_id(mongo_db: Database, db_table: str, item_id: str):
    id_filter = {"_id": ObjectId(item_id)}
    mongo_db[db_table].delete_one(id_filter)
    return


def delete_resource_item_by_filter(
    mongo_db: Database,
    db_table: str,
    filter: dict[str, Any] = {},
):
    mongo_db[db_table].delete_one(filter)
    return


def delete_resource_items_by_filter(
    mongo_db: Database,
    db_table: str,
    filter: dict[str, Any] = {},
):
    mongo_db[db_table].delete_many(filter)
    return
