import logging

from playwright.sync_api._generated import BrowserContext, Page
from playwright.sync_api import expect, Page
import allure

from test.admin_app_e2e_tests.screens.login_view_screen import LoginViewScreen
from test.admin_app_e2e_tests.screens.quotes_list_view_screen import QuotesListViewScreen
from test.admin_app_e2e_tests.screens.resources_dashboard_screen import ResourcesDashboardScreen
from test.admin_app_e2e_tests.screens.topbar_screen import TopbarScreen
from test.admin_app_e2e_tests.screens.user_notes_list_view_screen import UserNotesListViewScreen
from test.admin_app_e2e_tests.screens.users_list_view_screen import UsersListViewScreen
from test.admin_app_e2e_tests.screen_tasks.login_tasks import LoginTasks
from test.admin_app_e2e_tests.utils.playwright_screenshots import save_screenshot

logger = logging.getLogger(__name__)

class PageAndBrowserContextMissing(Exception):
    pass

class AdminUser:
    def __init__(
            self,
            name: str,
            email: str,
            password: str,
            base_url: str,
            page: Page = None,
            browser_context: BrowserContext = None,
        ):
        self.name = name
        self.email = email
        self.password = password
        self.base_url = base_url

        self.page = page
        self.browser_context = browser_context
        if not page and not self.browser_context:
            raise PageAndBrowserContextMissing(
                "Please provide playwright page or browser_context to AdminUser class on init"
            )

    def _initPage(self, browserName="default") -> Page:
        if not self.page:
            self.page = self.browser_context.new_page()

    def open_app_and_login(self):
        self._initPage()
        self.on_login_view().view_url.open()
        expect(self.page).to_have_title("vue_admin")
        self.with_login_tasks().login(self.email, self.password)
        self.on_resources_dashboard().view_url.expect_to_be_open()

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

    def on_users_list_views(self):
        return UsersListViewScreen(self.page, self.base_url, user_name=self.name)

    def on_quotes_list_views(self):
        return QuotesListViewScreen(self.page, self.base_url, user_name=self.name)

    def on_user_notes_list_views(self):
        return UserNotesListViewScreen(self.page, self.base_url, user_name=self.name)

    def with_login_tasks(self):
        return LoginTasks(self)
