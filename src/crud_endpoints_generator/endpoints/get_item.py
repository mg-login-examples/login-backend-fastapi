from typing import List, Any

from fastapi import status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base

def generate_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema
):
    @router.get("/{item_id}/", response_model=ResourceSchema, dependencies=dependencies)
    def get_resource_item(item_id: int, db: Session = db_as_dependency) -> ResourceSchema:
        item = crud_base.get_resource_item(db, ResourceModel, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item
