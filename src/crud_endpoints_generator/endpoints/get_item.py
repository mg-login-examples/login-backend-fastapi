from fastapi import status, HTTPException, APIRouter
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
    ResourceSchema: BaseSchema
):
    @router.get("/{item_id}/", response_model=ResourceSchema)
    def get_resource_item(
        item_id: int,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ) -> ResourceSchema:
        item = crud_base.get_resource_item(db, ResourceModel, item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item
