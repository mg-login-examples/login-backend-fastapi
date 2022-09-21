from typing import List, Any
from fastapi import status, Response, APIRouter
from sqlalchemy.orm import Session

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base

def generate_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies)
    def delete_item(item_id: int, db: Session = db_as_dependency):
        crud_base.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
