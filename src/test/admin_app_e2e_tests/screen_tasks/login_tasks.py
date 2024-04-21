import logging

import allure  # type: ignore

logger = logging.getLogger(__name__)


class LoginTasks:
    def __init__(self, user):
        # Import inside to avoid cyclic import error
        from test.admin_app_e2e_tests.users.admin_user import AdminUser

        self.user: AdminUser = user

    def login(self, email: str, password: str):
        step_desc = (
            f"User '{self.user.name}' login with email {email} and password {password}'"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.user.on_login_view().email_input.fill(email)
            self.user.on_login_view().email_input.expect_to_have_value(email)
            self.user.on_login_view().password_input.fill(password)
            self.user.on_login_view().password_input.expect_to_have_value(password)
            self.user.on_login_view().submit_button.click()

        step_wrapper()
