from typing import Callable

from fastapi import status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base
from data.schemas.users.user import User

def generate_endpoint(
    router: APIRouter,
    current_user_as_dependency: User,
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    customEndUserUpdateSchemaToDbSchema: Callable,
):
    @router.put("/{item_id}/", response_model=ResourceSchema)
    def update_item(
        item_id: int, item: ResourceSchema,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ) -> ResourceSchema:
        if item_id != item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        db_item = crud_base.update_resource_item_full(db, ResourceModel, item)
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

