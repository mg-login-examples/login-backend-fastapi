from fastapi import APIRouter
from typing import List

from api.admin.get_admin_router_for_model import get_admin_router_for_model
from api.admin.adminResourceModel import AdminResourceModel
from data.database.models import item as itemModel
from data.database.models import user as userModel
from data.schemas import items as itemSchemas
from data.schemas import users as userSchemas
from data import utils

router = APIRouter(prefix="/admin")

adminResources: List[AdminResourceModel] = [
    AdminResourceModel("items", itemSchemas.Item, itemSchemas.ItemCreate, itemModel.Item),
    AdminResourceModel("users", userSchemas.User, userSchemas.UserCreate, userModel.User, utils.userCreateSchemaToUserModel),
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
        infos.append(info)
    return infos
