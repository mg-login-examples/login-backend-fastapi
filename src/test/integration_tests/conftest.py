from test.integration_tests.fixtures.app import test_settings, test_app_db_manager, setup_db, test_client
from test.integration_tests.fixtures.quotes_admin import created_quote_by_admin, created_n_quotes_by_admin
from test.integration_tests.fixtures.users_admin import user_login, created_user_by_admin, created_n_users_by_admin

from test.integration_tests.fixtures.app import test_settings, test_app_db_manager, setup_db, test_client
from test.integration_tests.fixtures.login import login_response, test_client_logged_in, logged_in_user
from test.integration_tests.fixtures.quotes import created_quote, created_n_quotes