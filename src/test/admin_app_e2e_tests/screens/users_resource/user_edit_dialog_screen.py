from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper


class UserUpdateDialogScreen:
    def __init__(self, page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.user_name = user_name

    update_user_dialog_desc = "Update User Dialog"
    update_user_dialog_selector = "[test-id='update-item--title']:has-text('Update User')"

    @property
    def update_user_dialog(self):
        return PageSelectorHelper(
            self.page, self.update_user_dialog_selector, self.update_user_dialog_desc)

    user_email_input_desc = "User Email Input"
    user_email_input_selector = "[test-id='items--item-email--input']"

    @property
    def user_email_input(self):
        return PageSelectorHelper(
            self.page, self.user_email_input_selector, self.user_email_input_desc)

    update_user_button_desc = "Update User Button"
    update_user_button_selector = "[test-id='update-item--update-button']"

    @property
    def update_user_button(self):
        return PageSelectorHelper(
            self.page, self.update_user_button_selector, self.update_user_button_desc)
