from fastapi import APIRouter
from typing import List

from api.admin.get_admin_router_for_model import get_admin_router_for_model
from api.admin.adminResourceModel import AdminResourceModel
from api.admin.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties

from data.database.models.user import User as UserModel
from data.schemas.users.userDeep import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.endUserSchemasToDbSchemas.user import createSchemaToDbSchema as userCreateSchemaToDbSchema

from data.database.models.book import Book as BookModel
from data.schemas.books.bookDeep import Book as BookSchema
from data.schemas.books.bookCreate import BookCreate as BookCreateSchema
from data.endUserSchemasToDbSchemas.book import updateSchemaToDbSchema as bookUpdateSchemaToDbSchema

from data.database.models.movie import Movie as MovieModel
from data.schemas.movies.movieDeep import Movie as MovieSchema
from data.schemas.movies.movieCreate import MovieCreate as MovieCreateSchema
from data.endUserSchemasToDbSchemas.movie import updateSchemaToDbSchema as movieUpdateSchemaToDbSchema

from data.database.models.author import Author as AuthorModel
from data.schemas.authors.authorDeep import Author as AuthorSchema
from data.schemas.authors.authorCreate import AuthorCreate as AuthorCreateSchema


router = APIRouter(prefix="/admin")

adminResources: List[AdminResourceModel] = [
    AdminResourceModel(
        "users",
        UserSchema,
        UserCreateSchema,
        UserModel,
        customEndUserCreateSchemaToDbSchema=userCreateSchemaToDbSchema,
    ),
    AdminResourceModel(
        "books",
        BookSchema,
        BookCreateSchema,
        BookModel,
        customEndUserUpdateSchemaToDbSchema=bookUpdateSchemaToDbSchema,
    ),
    AdminResourceModel(
        "movies",
        MovieSchema,
        MovieCreateSchema,
        MovieModel,
        customEndUserUpdateSchemaToDbSchema=movieUpdateSchemaToDbSchema,
    ),
    AdminResourceModel(
        "authors",
        AuthorSchema,
        AuthorCreateSchema,
        AuthorModel,
    ),
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
