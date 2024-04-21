import logging

import allure  # type: ignore

from data.schemas.users.user import User

logger = logging.getLogger(__name__)


class UserResourceTasks:
    def __init__(self, user):
        # Import inside to avoid cyclic import error
        from test.admin_app_e2e_tests.users.admin_user import AdminUser

        self.user: AdminUser = user

    def create_basic_user(self, user_email: str, user_password: str):
        step_desc = f"User '{self.user.name}' create new user with email f'{user_email}' and password f'{user_password}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.user.with_resource_list_tasks().navigate_to_last_page()
            self.user.on_users_list_view().create_new_item_button.click()
            self.user.on_user_create_dialog().new_user_dialog.expect_to_be_visible()
            self.user.on_user_create_dialog().user_email_input.fill(user_email)
            self.user.on_user_create_dialog().user_email_input.expect_to_have_value(
                user_email
            )
            self.user.on_user_create_dialog().user_password_input.fill(user_password)
            self.user.on_user_create_dialog().user_password_input.expect_to_have_value(
                user_password
            )
            self.user.on_user_create_dialog().create_user_button.click()
            self.user.on_user_create_dialog().new_user_dialog.expect_not_to_be_visible()
            self.user.on_users_list_view().user_with_email(
                user_email
            ).expect_to_be_visible()

        step_wrapper()

    def create_full_user(self, user: User):
        pass
