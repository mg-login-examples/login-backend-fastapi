from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

class ResourcesDashboardScreen:
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = ViewUrlHelper(base_url + "/admin/", "Login Page", page, user_name=user_name)
        self.user_name = user_name

    users_resources_link_desc = "Users Resources Link"
    users_resources_link_selector = "[data-test='resources--users-link']"
    @property
    def users_resources_link(self):
        return PageSelectorHelper(self.page, self.users_resources_link_selector, self.users_resources_link_desc)
