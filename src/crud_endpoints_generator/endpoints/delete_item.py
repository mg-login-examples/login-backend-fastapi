from typing import Callable

from fastapi import Depends, status, Response, APIRouter
from sqlalchemy.orm import Session

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base


def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    get_db_session: Callable
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int, db: Session = Depends(get_db_session)):
        crud_base.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
