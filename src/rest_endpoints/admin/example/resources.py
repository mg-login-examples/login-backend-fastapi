from typing import List

from crud_endpoints_generator.resource_configurations import ResourceConfigurations

from data.database.models.examples.user import User as UserModel
from data.schemas.examples.users.userDeep import User as UserSchema
from data.schemas.examples.users.userCreate import UserCreate as UserCreateSchema
from data.endUserSchemasToDbSchemas.examples.user import createSchemaToDbSchema as userCreateSchemaToDbSchema

from data.database.models.examples.book import Book as BookModel
from data.schemas.examples.books.bookDeep import Book as BookSchema
from data.schemas.examples.books.bookCreate import BookCreate as BookCreateSchema
from data.endUserSchemasToDbSchemas.examples.book import updateSchemaToDbSchema as bookUpdateSchemaToDbSchema

from data.database.models.examples.movie import Movie as MovieModel
from data.schemas.examples.movies.movieDeep import Movie as MovieSchema
from data.schemas.examples.movies.movieCreate import MovieCreate as MovieCreateSchema
from data.endUserSchemasToDbSchemas.examples.movie import updateSchemaToDbSchema as movieUpdateSchemaToDbSchema

from data.database.models.examples.author import Author as AuthorModel
from data.schemas.examples.authors.authorDeep import Author as AuthorSchema
from data.schemas.examples.authors.authorCreate import AuthorCreate as AuthorCreateSchema


resources_configurations: List[ResourceConfigurations] = [
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

if not len({resource_configuration.resource_endpoints_url_prefix for resource_configuration in resources_configurations}) == len(resources_configurations):
    raise ValueError("2 or more Admin resources have the same url prefix! Ensure all url prefix are unique.")
