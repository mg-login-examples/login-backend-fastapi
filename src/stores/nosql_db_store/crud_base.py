from typing import List
from bson import ObjectId

from pymongo.database import Database
from pydantic import BaseModel

def get_resource_items_count(
    db: Database,
    db_table: str,
    filter: dict = {},
) -> int:
    items_count = db[db_table].count_documents(filter)
    return items_count

def get_resource_items(
    db: Database,
    db_table: str,
    filter: dict = {},
    ItemSchema: BaseModel = None,
    limit = 0,
    skip = 0,
) -> List[BaseModel] | List[dict]:
    items = []
    items_db = db[db_table].find(filter, limit=limit, skip=skip)
    if ItemSchema:
        for item_db in items_db:
            items.append(ItemSchema(**item_db))
    return items

def get_resource_item_by_filter(
    db: Database,
    db_table: str,
    filter: dict = {},
    ItemSchema: BaseModel = None
) -> BaseModel | dict:
    item_db = db[db_table].find_one(filter)
    item = ItemSchema(**item_db) if ItemSchema and item_db else item_db
    return item

def get_resource_item_by_id(
    db: Database,
    db_table: str,
    item_id: str,
    ItemSchema: BaseModel = None
) -> BaseModel | dict:
    id_filter = { "_id": ObjectId(item_id) }
    item_db = db[db_table].find_one(id_filter)
    item = ItemSchema(**item_db) if ItemSchema and item_db else item_db
    return item

def create_resource_item(
    db: Database,
    db_table: str,
    item_to_create: dict | BaseModel,
    ItemSchema: BaseModel = None
) -> BaseModel | dict:
    item_dict = item_to_create.model_dump() if isinstance(item_to_create, BaseModel) else item_to_create
    db[db_table].insert_one(item_dict)
    item_created = ItemSchema(**item_dict) if ItemSchema else item_dict
    return item_created

def update_item_by_id(
    db: Database,
    db_table: str,
    item_id: str,
    item_fields_to_update: dict | BaseModel,
):
    id_filter = { "_id": ObjectId(item_id) }
    item_fields_to_update = item_fields_to_update.model_dump() if isinstance(item_fields_to_update, BaseModel) else item_fields_to_update
    db[db_table].update_one(id_filter, { "$set": item_fields_to_update })
    return

def update_item_by_filter(
    db: Database,
    db_table: str,
    filter: dict,
    item_fields_to_update: dict | BaseModel,
):
    db[db_table].update_one(filter, { "$set": item_fields_to_update })
    return

def delete_resource_item_by_id(
    db: Database,
    db_table: str,
    item_id: str
):
    id_filter = { "_id": ObjectId(item_id) }
    db[db_table].delete_one(id_filter)
    return

def delete_resource_item_by_filter(
    db: Database,
    db_table: str,
    filter: dict = {},
):
    db[db_table].delete_one(filter)
    return

def delete_resource_items_by_filter(
    db: Database,
    db_table: str,
    filter: dict = {},
):
    db[db_table].delete_many(filter)
    return
