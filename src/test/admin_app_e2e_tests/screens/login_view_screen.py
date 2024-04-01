import logging

from playwright.sync_api import Page

from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

logger = logging.getLogger(__name__)


class LoginViewScreen:
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = ViewUrlHelper(
            base_url + "/admin/login/", "Login Page", page, user_name=user_name
        )
        self.user_name = user_name

    email_input_desc = "Email Input"
    email_input_selector = "[test-id='login--email-input']"

    @property
    def email_input(self):
        return PageSelectorHelper(
            self.page, self.email_input_selector, self.email_input_desc
        )

    password_input_desc = "Password Input"
    password_input_selector = "[test-id='login--password-input']"

    @property
    def password_input(self):
        return PageSelectorHelper(
            self.page, self.password_input_selector, self.password_input_desc
        )

    submit_button_desc = "Submit Button "
    submit_button_selector = "[test-id='login--submit-button']"

    @property
    def submit_button(self):
        return PageSelectorHelper(
            self.page, self.submit_button_selector, self.submit_button_desc
        )
