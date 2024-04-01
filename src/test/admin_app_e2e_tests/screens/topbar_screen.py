import logging
from test.admin_app_e2e_tests.utils.page_selector_helper import \
    PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

from playwright.sync_api import Page

logger = logging.getLogger(__name__)


class TopbarScreen:
    def __init__(self, page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.user_name = user_name

    home_link_desc = "Home Link"
    home_link_selector = "[test-id='topbar--router-link-home']"

    @property
    def home_link(self):
        return PageSelectorHelper(
            self.page, self.home_link_selector, self.home_link_desc
        )
