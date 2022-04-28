from typing import Callable

from fastapi import APIRouter
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
    ResourceCreateSchema: BaseSchema,
    customEndUserCreateSchemaToDbSchema: Callable,
):
    @router.post("/", response_model=ResourceSchema)
    def create_item(
        item: ResourceCreateSchema,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ) -> ResourceSchema:
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return crud_base.create_resource_item(db, ResourceModel, item)
