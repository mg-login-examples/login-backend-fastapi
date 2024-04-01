import logging
from test.admin_app_e2e_tests.screen_tasks.login_tasks import LoginTasks
from test.admin_app_e2e_tests.screen_tasks.resource_list_tasks import \
    ResourceListTasks
from test.admin_app_e2e_tests.screen_tasks.user_resource_tasks import \
    UserResourceTasks
from test.admin_app_e2e_tests.screens.login_view_screen import LoginViewScreen
from test.admin_app_e2e_tests.screens.quotes_resource.quotes_list_view_screen import \
    QuotesListViewScreen
from test.admin_app_e2e_tests.screens.resource_list_screen import \
    ResourceListViewScreen
from test.admin_app_e2e_tests.screens.resources_dashboard_screen import \
    ResourcesDashboardScreen
from test.admin_app_e2e_tests.screens.topbar_screen import TopbarScreen
from test.admin_app_e2e_tests.screens.user_notes_resource.user_notes_list_view_screen import \
    UserNotesListViewScreen
from test.admin_app_e2e_tests.screens.users_resource.user_create_dialog_screen import \
    UserCreateDialogScreen
from test.admin_app_e2e_tests.screens.users_resource.user_delete_dialog_screen import \
    UserDeleteDialogScreen
from test.admin_app_e2e_tests.screens.users_resource.user_edit_dialog_screen import \
    UserUpdateDialogScreen
from test.admin_app_e2e_tests.screens.users_resource.users_list_view_screen import \
    UsersListViewScreen
from test.admin_app_e2e_tests.utils.playwright_screenshots import \
    save_screenshot

import allure  # type: ignore
from playwright.sync_api import Page
from playwright.sync_api._generated import Page

logger = logging.getLogger(__name__)


class AdminUser:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        base_url: str,
        page: Page,
    ):
        self.name = name
        self.email = email
        self.password = password
        self.base_url = base_url

        self.page = page

    def save_screenshot(self):
        step_desc = f"User '{self.name}' save screenshot"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            save_screenshot(self.page, self.name)

        step_wrapper()

    def on_login_view(self):
        return LoginViewScreen(self.page, self.base_url, user_name=self.name)

    def on_topbar(self):
        return TopbarScreen(self.page, user_name=self.name)

    def on_resources_dashboard(self):
        return ResourcesDashboardScreen(self.page, self.base_url, user_name=self.name)

    def on_resource_list_view(self):
        return ResourceListViewScreen(self.page, user_name=self.name)

    def on_users_list_view(self):
        return UsersListViewScreen(self.page, self.base_url, user_name=self.name)

    def on_quotes_list_view(self):
        return QuotesListViewScreen(self.page, self.base_url, user_name=self.name)

    def on_user_notes_list_view(self):
        return UserNotesListViewScreen(self.page, self.base_url, user_name=self.name)

    def on_user_create_dialog(self):
        return UserCreateDialogScreen(self.page, user_name=self.name)

    def on_user_update_dialog(self):
        return UserUpdateDialogScreen(self.page, user_name=self.name)

    def on_user_delete_dialog(self):
        return UserDeleteDialogScreen(self.page, user_name=self.name)

    def with_login_tasks(self):
        return LoginTasks(self)

    def with_resource_list_tasks(self):
        return ResourceListTasks(self)

    def with_user_resource_tasks(self):
        return UserResourceTasks(self)
