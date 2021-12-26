from fastapi import APIRouter
from typing import List

from api.admin.get_admin_router_for_model import get_admin_router_for_model
from api.admin.adminResourceModel import AdminResourceModel
from api.admin.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties
from data.database.models.user import User as UserModel
from data.database.models.book import Book as BookModel
from data.database.models.movie import Movie as MovieModel
from data.schemas.users.userDeep import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.schemas import items as itemSchemas
from data.schemas.books.bookDeep import Book as BookSchema
from data.schemas.books.bookCreate import BookCreate as BookCreateSchema
from data.schemas.movies.movieDeep import Movie as MovieSchema
from data.schemas.movies.movieCreate import MovieCreate as MovieCreateSchema
from data.schemasToModels.user import userCreateSchemaToUserModel
from data.schemasToModels.movie import movieUpdateSchemaToMovieDict

router = APIRouter(prefix="/admin")

adminResources: List[AdminResourceModel] = [
    AdminResourceModel("users", UserSchema, UserCreateSchema, UserModel, customResourceCreateSchemaToResourceModel=userCreateSchemaToUserModel),
    AdminResourceModel("books", BookSchema, BookCreateSchema, BookModel),
    AdminResourceModel("movies", MovieSchema, MovieCreateSchema, MovieModel, customResourceUpdateSchemaToResourceSchemaDict=movieUpdateSchemaToMovieDict),
]

if not len({resource.url_id for resource in adminResources}) == len(adminResources):
    raise ValueError("2 or more Admin resources have the same urlId! Ensure all urlIds are unique.")

for resource in adminResources:
    router.include_router(get_admin_router_for_model(resource))

@router.get("/resources/")
def get_all_resources():
    infos = []
    for resource in adminResources:
        info = {
            "resourceUrlId": resource.url_id,
            "resourceName": resource.ResourceSchema.schema()["title"],
            "updateSchema": resource.ResourceSchema.schema(),
            "createSchema": resource.ResourceCreateSchema.schema(),
        }
        add_resource_url_ids_to_schema_properties(info["updateSchema"], resource, adminResources)
        infos.append(info)
    return infos
