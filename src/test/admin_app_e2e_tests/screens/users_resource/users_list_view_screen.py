from playwright.sync_api import Page
from test.admin_app_e2e_tests.screens.resource_list_screen import ResourceListViewScreen

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

class UsersListViewScreen(ResourceListViewScreen):
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        super().__init__(page, user_name=user_name)
        self.page = page
        self.view_url = ViewUrlHelper(base_url + "/admin/resource/users/", "Users List Page", page, user_name=user_name)
        self.user_name = user_name

    users_resources_title_desc = "Users Resources Title"
    users_resources_title_selector = "[data-test='items--title']:has-text('Users')"
    @property
    def users_resources_title(self):
        return PageSelectorHelper(self.page, self.users_resources_title_selector, self.users_resources_title_desc)

    @staticmethod
    def user_with_email_desc(email: str):
        return f"User with email '{email}'"
    @staticmethod
    def user_with_email_selector(email: str):
        return f"[data-test='items--item']:has-text('{email}')"
    def user_with_email(self, email: str):
        return PageSelectorHelper(self.page, UsersListViewScreen.user_with_email_selector(email), UsersListViewScreen.user_with_email_desc(email))

    @staticmethod
    def user_update_button_desc(designation: str):
        return f"User '{designation}' Update Button"
    @staticmethod
    def user_update_button_selector(designation: str):
        return f"[data-test='items--item']:has-text('{designation}') [data-test='items--edit-item']"
    def user_update_button(self, designation: str):
        return PageSelectorHelper(self.page, UsersListViewScreen.user_update_button_selector(designation), UsersListViewScreen.user_update_button_desc(designation))

    @staticmethod
    def user_delete_button_desc(designation: str):
        return f"User '{designation}' Delete Button"
    @staticmethod
    def user_delete_button_selector(designation: str):
        return f"[data-test='items--item']:has-text('{designation}') [data-test='items--delete-item']"
    def user_delete_button(self, designation: str):
        return PageSelectorHelper(self.page, UsersListViewScreen.user_delete_button_selector(designation), UsersListViewScreen.user_delete_button_selector(designation))
