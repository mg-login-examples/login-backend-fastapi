from typing import Callable, Type
from pydantic import BaseModel as BaseSchema

from sqlalchemy.ext.declarative import DeclarativeMeta


class ResourceConfigurations:

    def __init__(
        self,
        resource_endpoints_url_prefix,
        ResourceSchema: Type[BaseSchema],
        ResourceCreateSchema: Type[BaseSchema],
        ResourceModel: Type[DeclarativeMeta] | None = None,
        MongoDBTable: str | None = None,
        readonly_fields: list[str] | None = None,
        designation_fields: list[str] | None = None,
        customEndUserCreateSchemaToDbSchema: Callable | None = None,
        customEndUserUpdateSchemaToDbSchema: Callable | None = None,
    ):
        self.resource_endpoints_url_prefix = resource_endpoints_url_prefix
        self.ResourceSchema = ResourceSchema
        self.ResourceCreateSchema = ResourceCreateSchema
        self.ResourceModel = ResourceModel
        self.MongoDBTable = MongoDBTable
        self.readonly_fields = readonly_fields if readonly_fields is not None else [
            "id"]
        self.designation_fields = designation_fields if designation_fields else []
        self.customEndUserCreateSchemaToDbSchema = customEndUserCreateSchemaToDbSchema
        self.customEndUserUpdateSchemaToDbSchema = customEndUserUpdateSchemaToDbSchema

        if not ResourceModel and not MongoDBTable:
            raise Exception(f"Both ResourceModel and MongoDBTable are None for resource {
                            resource_endpoints_url_prefix}")
