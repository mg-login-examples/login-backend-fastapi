from typing import Callable
from pydantic import BaseModel as BaseSchema

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel

class ResourceConfigurations:

    def __init__(
        self,
        resource_endpoints_url_prefix,
        ResourceSchema: BaseSchema,
        ResourceCreateSchema: BaseSchema,
        ResourceModel: BaseORMModel = None,
        MongoDBTable: str = None,
        customEndUserCreateSchemaToDbSchema: Callable = None,
        customEndUserUpdateSchemaToDbSchema: Callable = None,
    ):
        self.resource_endpoints_url_prefix = resource_endpoints_url_prefix
        self.ResourceSchema = ResourceSchema
        self.ResourceCreateSchema = ResourceCreateSchema
        self.ResourceModel = ResourceModel
        self.MongoDBTable = MongoDBTable
        self.customEndUserCreateSchemaToDbSchema = customEndUserCreateSchemaToDbSchema
        self.customEndUserUpdateSchemaToDbSchema = customEndUserUpdateSchemaToDbSchema

        if not ResourceModel and not MongoDBTable:
            raise Exception(f"Both ResourceModel and MongoDBTable are None for resource {resource_endpoints_url_prefix}")
