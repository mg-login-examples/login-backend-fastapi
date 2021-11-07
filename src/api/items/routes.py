from typing import List
import random
import string

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from data.database.dbManager import db_manager
from data.crud import items as crudItems
from data.schemas import items as itemSchemas

router = APIRouter(prefix="/items")

@router.get("/{item_id}/", response_model=itemSchemas.Item)
def get_item(item_id: int, db: Session = Depends(db_manager.get_db_session)) -> itemSchemas.Item:
    item = crudItems.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.get("/", response_model=List[itemSchemas.Item])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(db_manager.get_db_session)) -> List[itemSchemas.Item]:
    return crudItems.get_items(db, skip=skip, limit=limit)

@router.post("/", response_model=itemSchemas.Item)
def create_item(item: itemSchemas.ItemCreate, db: Session = Depends(db_manager.get_db_session)) -> itemSchemas.Item:
    return crudItems.create_item(db=db, item=item)

@router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(db_manager.get_db_session)):
    crudItems.delete_item(db, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
