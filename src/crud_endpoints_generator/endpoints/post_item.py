from typing import Callable

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base


def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    ResourceCreateSchema: BaseSchema,
    customEndUserCreateSchemaToDbSchema: Callable,
    get_db_session: Callable
):
    @router.post("/", response_model=ResourceSchema)
    def create_item(item: ResourceCreateSchema, db: Session = Depends(get_db_session)) -> ResourceSchema:
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return crud_base.create_resource_item(db, ResourceModel, item)
