import pytest
from _pytest.fixtures import FixtureRequest

from playwright.sync_api._generated import BrowserContext, Page

from test.admin_app_e2e_tests.users.admin_user import AdminUser
from test.env_settings_test import EnvSettingsTest

from pytest import StashKey, CollectReport
from typing import Dict
import logging

logger = logging.getLogger(__name__)

phase_report_key = StashKey[Dict[str, CollectReport]]()

@pytest.fixture
@pytest.mark.timeout(30)
def admin_user_not_logged_in(
    # my_playwright_context: BrowserContext,
    page: Page,
    env_settings_test: EnvSettingsTest,
    request: FixtureRequest
):
    user = AdminUser(
        "mr admin",
        env_settings_test.admin_user_email,
        env_settings_test.admin_user_password,
        env_settings_test.playwright_app_base_url,
        # browser_context=my_playwright_context
        page=page
    )
    yield user
    try:
        if hasattr(request.node, "rep_call"):
            outcome = request.node.rep_call
            # if outcome.failed:
            #     logger.info(f"Test {request.node.name} failed. Taking screenshot")
            #     user.save_screenshot()
    except Exception as e:
        logger.error("Error in admin user fixture teardown")
        logger.error(e)

@pytest.fixture
def admin_user(admin_user_not_logged_in: AdminUser):
    admin_user_not_logged_in.open_app_and_login()
    return admin_user_not_logged_in
