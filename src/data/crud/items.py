from typing import List
from sqlalchemy.orm import Session

from data.schemas import items as itemsSchemas
from data.database.models.item import Item as ItemModel
from data.crud import base as baseCrud


def get_item(db: Session, item_id: int) -> ItemModel:
    return baseCrud.get_resource_item(db, ItemModel, item_id)

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[ItemModel]:
    return baseCrud.get_resource_items(db, ItemModel, skip = skip, limit = limit)

def create_item(db: Session, item: itemsSchemas.ItemCreate) -> ItemModel:
    db_item = ItemModel(**item.dict())
    return baseCrud.create_resource_item(db, db_item)

def delete_item(db: Session, item_id: int):
    baseCrud.delete_resource_item(db, ItemModel, item_id)

# def create_user_item(db: Session, item: itemsSchemas.ItemCreate, user_id: int) -> ItemModel:
#     db_item = ItemModel(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
