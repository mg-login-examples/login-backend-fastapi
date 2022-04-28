from fastapi import status, Response, APIRouter
from sqlalchemy.orm import Session

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base
from data.schemas.users.user import User

def generate_endpoint(
    router: APIRouter,
    current_user_as_dependency: User,
    db_as_dependency: Session,
    ResourceModel: BaseORMModel
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        item_id: int,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ):
        crud_base.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
