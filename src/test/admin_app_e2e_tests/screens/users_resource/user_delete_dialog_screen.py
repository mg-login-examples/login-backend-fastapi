from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper

class UserDeleteDialogScreen:
    def __init__(self, page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.user_name = user_name

    delete_user_dialog_desc = "Delete User Dialog"
    delete_user_dialog_selector = "[data-test='items--delete-item-dialog']:has-text('Delete User')"
    @property
    def delete_user_dialog(self):
        return PageSelectorHelper(self.page, self.delete_user_dialog_selector, self.delete_user_dialog_desc)

    @staticmethod
    def delete_user_message_desc(user_designation: str):
        return f"Delete message for user with name or email '{user_designation}'s"
    @staticmethod
    def delete_user_message_selector(user_designation: str):
        return f"[data-test='items--delete-item-dialog--delete-message']:has-text('{user_designation}')"
    def delete_user_message(self, user_designation: str):
        return PageSelectorHelper(self.page, UserDeleteDialogScreen.delete_user_message_selector(user_designation), UserDeleteDialogScreen.delete_user_message_desc(user_designation))

    delete_user_button_desc = "Delete User Button"
    delete_user_button_selector = "[data-test='items--delete-item-dialog--delete']"
    @property
    def delete_user_button(self):
        return PageSelectorHelper(self.page, self.delete_user_button_selector, self.delete_user_button_desc)
