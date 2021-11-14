from fastapi import APIRouter

from api.admin.get_admin_router_for_model import get_admin_router_for_model

from data.database.models import item as itemModel
from data.database.models import user as userModel
from data.schemas import items as itemSchemas
from data.schemas import users as userSchemas

router = APIRouter(prefix="/api")

router.include_router(get_admin_router_for_model("items", itemSchemas.Item, itemSchemas.ItemCreate, itemModel.Item))
