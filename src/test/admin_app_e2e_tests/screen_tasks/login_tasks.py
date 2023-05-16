import logging

import allure

logger = logging.getLogger(__name__)

class LoginTasks:
    def __init__(self, user):
        from test.admin_app_e2e_tests.users.admin_user import AdminUser
        self.user: AdminUser = user

    def login(self, email: str, password: str):
        step_desc = f"User '{self.user.name}' login with email {email} and password {password}'"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.user.on_login_view().email_input.type(email)
            self.user.on_login_view().email_input.expectToHaveValue(email)
            self.user.on_login_view().password_input.type(password)
            self.user.on_login_view().password_input.expectToHaveValue(password)
            self.user.on_login_view().submit_button.click()
        step_wrapper()