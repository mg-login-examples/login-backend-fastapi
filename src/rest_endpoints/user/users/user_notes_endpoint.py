from typing import Any

from pymongo.database import Database

from helpers_classes.custom_api_router import APIRouter
from stores.nosql_db_store import crud_base
from data.mongo_schemas.user_notes.user_note import UserNote


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Database,
    restrict_endpoint_to_own_resources_param_user_id: Any,
):

    @router.get(
        "/{user_id}/user-notes",
        response_model=list[UserNote],
        response_model_by_alias=False,
        dependencies=[restrict_endpoint_to_own_resources_param_user_id],
    )
    async def get_user_notes_of_user(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        sql_db_session: Database = sql_db_session_as_dependency,
    ):
        user_notes = crud_base.get_resource_items_pydantized(
            sql_db_session,
            "user_notes",
            UserNote,
            filter={"user_id": user_id},
            skip=skip,
            limit=limit,
        )
        return user_notes
