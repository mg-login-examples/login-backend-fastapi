from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

class UsersListViewScreen:
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = ViewUrlHelper(base_url + "/admin/resource/users", "Users List Page", page, user_name=user_name)
        self.user_name = user_name
