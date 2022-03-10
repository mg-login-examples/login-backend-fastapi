from typing import Callable

from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base


def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    get_db_session: Callable
):
    @router.get("/{item_id}/", response_model=ResourceSchema)
    def get_resource_item(item_id: int, db: Session = Depends(get_db_session)) -> ResourceSchema:
        item = crud_base.get_resource_item(db, ResourceModel, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item
