from typing import Callable
from pydantic import BaseModel as BaseSchema

from .sqlalchemy_base_model import Base as BaseORMModel

class ResourceConfigurations:

    def __init__(
        self,
        resource_endpoints_url_prefix,
        ResourceSchema: BaseSchema,
        ResourceCreateSchema: BaseSchema,
        ResourceModel: BaseORMModel,
        customEndUserCreateSchemaToDbSchema: Callable = None,
        customEndUserUpdateSchemaToDbSchema: Callable = None,
    ):
        self.resource_endpoints_url_prefix = resource_endpoints_url_prefix
        self.ResourceSchema = ResourceSchema
        self.ResourceCreateSchema = ResourceCreateSchema
        self.ResourceModel = ResourceModel
        self.customEndUserCreateSchemaToDbSchema = customEndUserCreateSchemaToDbSchema
        self.customEndUserUpdateSchemaToDbSchema = customEndUserUpdateSchemaToDbSchema
