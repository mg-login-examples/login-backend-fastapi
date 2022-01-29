from typing import Callable
from pydantic import BaseModel as BaseSchema

from data.database.models.base import Base as BaseORMModel


class AdminResourceModel:
    def __init__(
        self,
        url_id: str,
        ResourceSchema: BaseSchema,
        ResourceCreateSchema: BaseSchema,
        ResourceModel: BaseORMModel,
        customEndUserCreateSchemaToDbSchema: Callable = None,
        customEndUserUpdateSchemaToDbSchema: Callable = None,
    ):
        self.url_id = url_id
        self.ResourceSchema = ResourceSchema
        self.ResourceCreateSchema = ResourceCreateSchema
        self.ResourceModel = ResourceModel
        self.customEndUserCreateSchemaToDbSchema = customEndUserCreateSchemaToDbSchema
        self.customEndUserUpdateSchemaToDbSchema = customEndUserUpdateSchemaToDbSchema
