import pytest
from _pytest.fixtures import FixtureRequest
import logging

from playwright.sync_api._generated import Page
from playwright.sync_api import expect

from test.admin_app_e2e_tests.users.admin_user import AdminUser
from test.env_settings_test import EnvSettingsTest

logger = logging.getLogger(__name__)

@pytest.fixture
def admin_user_not_logged_in(
    page: Page,
    env_settings_test: EnvSettingsTest,
    request: FixtureRequest
):
    user = AdminUser(
        "Test Admin",
        env_settings_test.admin_user_email,
        env_settings_test.admin_user_password,
        env_settings_test.playwright_app_base_url,
        page=page
    )
    yield user
    try:
        if hasattr(request.node, "rep_call"):
            outcome = request.node.rep_call
            if outcome.failed:
                logger.info(f"Test {request.node.name} failed. Taking screenshot")
                user.save_screenshot()
    except Exception as e:
        logger.error("Error in admin user fixture teardown")
        logger.error(e)

@pytest.fixture
def admin_user(admin_user_not_logged_in: AdminUser):
    admin_user_not_logged_in.on_login_view().view_url.open()
    expect(admin_user_not_logged_in.page).to_have_title("Admin App")
    admin_user_not_logged_in.with_login_tasks().login(admin_user_not_logged_in.email, admin_user_not_logged_in.password)
    admin_user_not_logged_in.on_resources_dashboard().view_url.expect_to_be_open()
    return admin_user_not_logged_in
