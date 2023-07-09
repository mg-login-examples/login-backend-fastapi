from typing import Callable, List
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
        readonly_fields: List[str] = None,
        designation_fields: List[str] = None,
        customEndUserCreateSchemaToDbSchema: Callable = None,
        customEndUserUpdateSchemaToDbSchema: Callable = None,
    ):
        self.resource_endpoints_url_prefix = resource_endpoints_url_prefix
        self.ResourceSchema = ResourceSchema
        self.ResourceCreateSchema = ResourceCreateSchema
        self.ResourceModel = ResourceModel
        self.MongoDBTable = MongoDBTable
        self.readonly_fields = readonly_fields if readonly_fields else ["id"]
        self.designation_fields = designation_fields
        self.customEndUserCreateSchemaToDbSchema = customEndUserCreateSchemaToDbSchema
        self.customEndUserUpdateSchemaToDbSchema = customEndUserUpdateSchemaToDbSchema

        if not ResourceModel and not MongoDBTable:
            raise Exception(f"Both ResourceModel and MongoDBTable are None for resource {resource_endpoints_url_prefix}")
