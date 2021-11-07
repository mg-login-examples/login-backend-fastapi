from typing import List
from sqlalchemy.orm import Session

from data.schemas import items as itemsSchemas
from data.database.models.item import Item as ItemModel


def get_item(db: Session, item_id: int) -> ItemModel:
    return db.query(ItemModel).filter(ItemModel.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[ItemModel]:
    return db.query(ItemModel).offset(skip).limit(limit).all()

def create_item(db: Session, item: itemsSchemas.ItemCreate) -> ItemModel:
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db.query(ItemModel).filter(ItemModel.id == item_id).delete()
    db.commit()

# def create_user_item(db: Session, item: itemsSchemas.ItemCreate, user_id: int) -> ItemModel:
#     db_item = ItemModel(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
