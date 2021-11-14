from typing import List

from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from pydantic import BaseModel as BaseSchema

from app_configurations import app_db_manager
from data.crud import base as crudBase
from data.database.models.base import Base as BaseORMModel


def get_admin_router_for_model(url_tag: str, ResourceSchema: BaseSchema, ResourceCreateSchema: BaseSchema, ResourceModel: BaseORMModel):
    router = APIRouter(prefix=f"/{url_tag}")

    @router.get("/{item_id}/", response_model=ResourceSchema)
    def get_resource_item(item_id: int, db: Session = Depends(app_db_manager.db_session)) -> ResourceSchema:
        item = crudBase.get_resource_item(db, ResourceModel, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item

    @router.get("/", response_model=List[ResourceSchema])
    def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(app_db_manager.db_session)) -> List[ResourceSchema]:
        return crudBase.get_resource_items(db, ResourceModel, skip=skip, limit=limit)

    @router.post("/", response_model=ResourceSchema)
    def create_item(item: ResourceCreateSchema, db: Session = Depends(app_db_manager.db_session)) -> ResourceSchema:
        db_item = ResourceModel(**item.dict())
        return crudBase.create_resource_item(db, db_item)

    @router.put("/{item_id}/", response_model=ResourceSchema)
    def update_item(item_id: int, item: ResourceSchema, db: Session = Depends(app_db_manager.db_session)) -> ResourceSchema:
        if item_id != item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if not crudBase.get_resource_item_by_attribute(db, ResourceModel, "id", item_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return crudBase.update_resource_item(db, ResourceModel, item.dict())

    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(app_db_manager.db_session)):
        crudBase.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
