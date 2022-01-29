from typing import List

from fastapi import APIRouter, status, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from api.admin.adminResourceModel import AdminResourceModel
from app_configurations import app_db_manager
from data.crud import base as crudBase


def get_admin_router_for_model(resource: AdminResourceModel):
    router = APIRouter(prefix=f"/resource/{resource.url_id}")

    ResourceSchema = resource.ResourceSchema
    ResourceCreateSchema = resource.ResourceCreateSchema
    customEndUserCreateSchemaToDbSchema = resource.customEndUserCreateSchemaToDbSchema
    customEndUserUpdateSchemaToDbSchema = resource.customEndUserUpdateSchemaToDbSchema
    ResourceModel = resource.ResourceModel

    @router.get("/count/", response_model=int)
    def get_resource_items_count(db: Session = Depends(app_db_manager.db_session)) -> int:
        totalItemsCount = crudBase.get_resource_items_count(db, ResourceModel)
        return totalItemsCount

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
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return crudBase.create_resource_item(db, ResourceModel, item)

    @router.put("/{item_id}/", response_model=ResourceSchema)
    def update_item(item_id: int, item: ResourceSchema, db: Session = Depends(app_db_manager.db_session)) -> ResourceSchema:
        if item_id != item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        db_item = crudBase.update_resource_item_full(db, ResourceModel, item)
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return db_item

    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(app_db_manager.db_session)):
        crudBase.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router
