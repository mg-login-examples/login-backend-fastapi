from typing import Callable

from fastapi import Depends, status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base


def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    customEndUserUpdateSchemaToDbSchema: Callable,
    get_db_session: Callable
):
    @router.put("/{item_id}/", response_model=ResourceSchema)
    def update_item(item_id: int, item: ResourceSchema, db: Session = Depends(get_db_session)) -> ResourceSchema:
        if item_id != item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        db_item = crud_base.update_resource_item_full(db, ResourceModel, item)
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

