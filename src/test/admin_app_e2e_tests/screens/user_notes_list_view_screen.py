from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

class UserNotesListViewScreen:
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = ViewUrlHelper(base_url + "/admin/resource/user-notes", "User Notes List Page", page, user_name=user_name)
        self.user_name = user_name

    user_notes_resources_title_desc = "User Notes Resources Title"
    user_notes_resources_title_selector = "[data-test='items--title']"
    @property
    def user_notes_resources_title(self):
        return PageSelectorHelper(self.page, self.user_notes_resources_title_selector, self.user_notes_resources_title_desc)