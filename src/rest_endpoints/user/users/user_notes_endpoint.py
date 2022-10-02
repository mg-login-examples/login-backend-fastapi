from typing import List, Any

from pymongo.database import Database

from helpers_classes.custom_api_router import APIRouter
from stores.nosql_db_store import crud_base
from data.mongo_schemas.user_notes.user_note import UserNote

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Database,
    restrict_endpoint_to_own_resources_param_user_id: Any
):

    @router.get('/{user_id}/user-notes', response_model=List[UserNote], response_model_by_alias=False, dependencies=[restrict_endpoint_to_own_resources_param_user_id])
    async def get_user_notes_of_user(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Database = db_as_dependency,
    ):
        user_notes = crud_base.get_resource_items(
            db,
            "user_notes",
            filter={ "user_id": user_id },
            ItemSchema=UserNote,
            skip=skip,
            limit=limit,
        )
        return user_notes