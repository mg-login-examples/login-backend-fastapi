from test.admin_app_e2e_tests.utils.page_selector_helper import \
    PageSelectorHelper

from playwright.sync_api import Page


class UserCreateDialogScreen:
    def __init__(self, page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.user_name = user_name

    new_user_dialog_desc = "New User Dialog"
    new_user_dialog_selector = "[test-id='create-item--title']:has-text('Create User')"

    @property
    def new_user_dialog(self):
        return PageSelectorHelper(
            self.page, self.new_user_dialog_selector, self.new_user_dialog_desc
        )

    user_email_input_desc = "User Email Input"
    user_email_input_selector = "[test-id='items--item-email--input']"

    @property
    def user_email_input(self):
        return PageSelectorHelper(
            self.page, self.user_email_input_selector, self.user_email_input_desc
        )

    user_password_input_desc = "User Password Input"
    user_password_input_selector = "[test-id='items--item-password--input']"

    @property
    def user_password_input(self):
        return PageSelectorHelper(
            self.page, self.user_password_input_selector, self.user_password_input_desc
        )

    create_user_button_desc = "Create User Button"
    create_user_button_selector = "[test-id='create-item--create-button']"

    @property
    def create_user_button(self):
        return PageSelectorHelper(
            self.page, self.create_user_button_selector, self.create_user_button_desc
        )
