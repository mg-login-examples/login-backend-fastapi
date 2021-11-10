from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app_configurations import app_db_manager
from data.crud import items as crudItems
from data.schemas import items as itemSchemas

router = APIRouter()

@router.get("/users/{user_id}/items/", response_model=List[itemSchemas.Item])
def get_user_items(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(app_db_manager.db_session)) -> List[itemSchemas.Item]:
    # TODO add get_user_item CRUD
    items = crudItems.get_items(db, skip=skip, limit=limit)
    return items
