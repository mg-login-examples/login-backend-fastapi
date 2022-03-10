from fastapi import APIRouter
from typing import List

from crud_endpoints_generator.crud_endpoints_generator import get_resource_endpoints_router
from crud_endpoints_generator.endpoints_required import Endpoints
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from admin.api.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties
from app_configurations import app_db_manager

from data.database.models.examples.user import User as UserModel
from admin.data.schemas.examples.users.userDeep import User as UserSchema
from admin.data.schemas.examples.users.userCreate import UserCreate as UserCreateSchema
from admin.data.endUserSchemasToDbSchemas.examples.user import createSchemaToDbSchema as userCreateSchemaToDbSchema

from data.database.models.examples.book import Book as BookModel
from admin.data.schemas.examples.books.bookDeep import Book as BookSchema
from admin.data.schemas.examples.books.bookCreate import BookCreate as BookCreateSchema
from admin.data.endUserSchemasToDbSchemas.examples.book import updateSchemaToDbSchema as bookUpdateSchemaToDbSchema

from data.database.models.examples.movie import Movie as MovieModel
from admin.data.schemas.examples.movies.movieDeep import Movie as MovieSchema
from admin.data.schemas.examples.movies.movieCreate import MovieCreate as MovieCreateSchema
from admin.data.endUserSchemasToDbSchemas.examples.movie import updateSchemaToDbSchema as movieUpdateSchemaToDbSchema

from data.database.models.examples.author import Author as AuthorModel
from admin.data.schemas.examples.authors.authorDeep import Author as AuthorSchema
from admin.data.schemas.examples.authors.authorCreate import AuthorCreate as AuthorCreateSchema


router = APIRouter(prefix="/admin")

resourcesConfigurations: List[ResourceConfigurations] = [
    ResourceConfigurations(
        "users",
        UserSchema,
        UserCreateSchema,
        UserModel,
        customEndUserCreateSchemaToDbSchema=userCreateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "books",
        BookSchema,
        BookCreateSchema,
        BookModel,
        customEndUserUpdateSchemaToDbSchema=bookUpdateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "movies",
        MovieSchema,
        MovieCreateSchema,
        MovieModel,
        customEndUserUpdateSchemaToDbSchema=movieUpdateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "authors",
        AuthorSchema,
        AuthorCreateSchema,
        AuthorModel,
    ),
]

if not len({resourceConfiguration.resource_endpoints_url_prefix for resourceConfiguration in resourcesConfigurations}) == len(resourcesConfigurations):
    raise ValueError("2 or more Admin resources have the same url prefix! Ensure all url prefix are unique.")

endpoints_required = Endpoints().require_all()
for resourceConfiguration in resourcesConfigurations:
    router.include_router(
        get_resource_endpoints_router(
            endpoints_required,
            resourceConfiguration,
            app_db_manager.db_session
        )
    )

@router.get("/resources/")
def get_all_resources():
    infos = []
    for resourceConfiguration in resourcesConfigurations:
        info = {
            "resourceUrlId": resourceConfiguration.resource_endpoints_url_prefix,
            "resourceName": resourceConfiguration.ResourceSchema.schema()["title"],
            "updateSchema": resourceConfiguration.ResourceSchema.schema(),
            "createSchema": resourceConfiguration.ResourceCreateSchema.schema(),
        }
        add_resource_url_ids_to_schema_properties(info["updateSchema"], resourceConfiguration, resourcesConfigurations)
        infos.append(info)
    return infos
