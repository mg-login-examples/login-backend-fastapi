from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from data.database.dbManager import db_manager
from data.crud import items as crudItems
from data.schemas import items as itemSchemas

router = APIRouter()

@router.get("/users/{userid}/items/", response_model=itemSchemas.Item)
def get_user_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(db_manager.get_db_session)) -> List[itemSchemas.Item]:
    # TODO add get_user_item CRUD
    items = crudItems.get_items(db, skip=skip, limit=limit)
    return items
