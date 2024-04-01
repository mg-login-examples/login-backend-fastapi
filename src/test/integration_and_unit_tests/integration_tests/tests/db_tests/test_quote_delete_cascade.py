import logging
from test.integration_and_unit_tests.integration_tests.utils.fake_quote import \
    generate_random_quote_to_create
from test.integration_and_unit_tests.integration_tests.utils.fake_user import \
    generate_random_user_to_create

from data.database.models.quote import Quote as QuoteModel
from data.database.models.user import User as UserModel
from data.database.models.user_quote_like import \
    UserQuoteLike as UserQuoteLikeModel
from data.endUserSchemasToDbSchemas.quote import \
    createSchemaToDbSchema as quoteCreateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.user import \
    createSchemaToDbSchema as userCreateSchemaToDbSchema
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep
from data.schemas.user_quote_like.user_quote_like import UserQuoteLike
from data.schemas.users.userDeep import User as UserDeep
from stores.sql_db_store import crud_base
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager

logger = logging.getLogger(__name__)


def test_quote_delete_cascade_quote_likes(app_db_manager: SQLAlchemyDBManager):
    db_session = next(app_db_manager.db_session())
    # create user (quote author) and quote
    user_login = generate_random_user_to_create()
    user_password_hashed = userCreateSchemaToDbSchema(user_login)
    user_db = crud_base.create_resource_item(
        db_session, UserModel, user_password_hashed
    )
    user = UserDeep.model_validate(user_db)
    quote_to_create = generate_random_quote_to_create(user)
    quote_to_create_for_db = quoteCreateSchemaToDbSchema(quote_to_create)
    quote_db = crud_base.create_resource_item(
        db_session, QuoteModel, quote_to_create_for_db
    )
    quote = QuoteDeep.model_validate(quote_db)
    # create user 2 and quote like
    user_2_login = generate_random_user_to_create()
    user_2_password_hashed = userCreateSchemaToDbSchema(user_2_login)
    user_2_db = crud_base.create_resource_item(
        db_session, UserModel, user_2_password_hashed
    )
    user_2 = UserDeep.model_validate(user_2_db)
    user_quote_like = UserQuoteLike(user_id=user_2.id, quote_id=quote.id)
    crud_base.create_resource_item(db_session, UserQuoteLikeModel, user_quote_like)
    # given a quote with quote likes
    quote_db = crud_base.get_resource_item(db_session, QuoteModel, quote.id)
    quote = QuoteDeep.model_validate(quote_db)
    assert len(quote.liked_by_users) == 1
    assert quote.liked_by_users[0].id == user_2.id
    # if the quote is deleted
    crud_base.delete_resource_item(db_session, QuoteModel, quote.id)
    quote_db = crud_base.get_resource_item(db_session, QuoteModel, quote.id)
    assert quote_db is None
    # the quote's user likes are also deleted
    user_2_db = crud_base.get_resource_item(db_session, UserModel, user_2.id)
    user_2 = UserDeep.model_validate(user_2_db)
    assert len(user_2.liked_quotes) == 0
    user_quote_like = crud_base.get_resource_item_by_attribute(
        db_session, UserQuoteLikeModel, UserQuoteLikeModel.quote_id, quote.id
    )
    assert user_quote_like is None
    user_quote_like = crud_base.get_resource_item_by_attribute(
        db_session, UserQuoteLikeModel, UserQuoteLikeModel.user_id, user_2.id
    )
    assert user_quote_like is None
