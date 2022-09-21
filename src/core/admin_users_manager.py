import logging

from sqlalchemy.orm import Session

from stores.sql_db_store import crud_base
from data.database.models.admin_user import AdminUser as AdminUserModel
from data.schemas.admin_users.admin_user_create_as_model import AdminUserCreateAsModel as AdminUserCreateAsModelSchema
from data.schemas.admin_users.admin_user import AdminUser as AdminUserSchema
from data.schemas.admin_users.admin_user_with_password import AdminUserWithPassword as AdminUserWithPasswordSchema
from utils.security.password_utils import get_password_hash

logger = logging.getLogger(__name__)

def create_admin_user(email: str, password: str, db: Session):
    hashed_password = get_password_hash(password)
    admin_user = AdminUserCreateAsModelSchema(email=email, hashed_password=hashed_password)
    admin_user_created = crud_base.create_resource_item(db, AdminUserModel, admin_user)
    admin_user_schema = AdminUserSchema.from_orm(admin_user_created)
    logger.info("Admin user created:")
    logger.info(admin_user_schema.dict())

def update_admin_user_password(email: str, password_new: str, db: Session):
    admin_user = crud_base.get_resource_item_by_attribute(db, AdminUserModel, AdminUserModel.email, email)
    admin_user = AdminUserWithPasswordSchema.from_orm(admin_user)
    admin_user.hashed_password = get_password_hash(password_new)
    admin_user_updated = crud_base.update_resource_item_full(db, AdminUserModel, admin_user)
    admin_user_schema = AdminUserSchema.from_orm(admin_user_updated)
    logger.info("Admin user updated:")
    logger.info(admin_user_schema.dict())

def delete_admin_user(email: str, db: Session):
    crud_base.delete_resource_item_by_attribute(db, AdminUserModel, AdminUserModel.email, email)
    logger.info(f"Admin user with email '{email}' has been deleted.")
