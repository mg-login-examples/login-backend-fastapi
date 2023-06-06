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

    quotes_resources_link_desc = "Quotes Resources Link"
    quotes_resources_link_selector = "[data-test='resources--quotes-link']"
    @property
    def quotes_resources_link(self):
        return PageSelectorHelper(self.page, self.quotes_resources_link_selector, self.quotes_resources_link_desc)

    user_notes_resources_link_desc = "User Notes Resources Link"
    user_notes_resources_link_selector = "[data-test='resources--user-notes-link']"
    @property
    def user_notes_resources_link(self):
        return PageSelectorHelper(self.page, self.user_notes_resources_link_selector, self.user_notes_resources_link_desc)
