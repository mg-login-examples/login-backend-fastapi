from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper
from test.admin_app_e2e_tests.utils.view_url_helper import ViewUrlHelper

from playwright.sync_api import Page


class QuotesListViewScreen:
    def __init__(self, page: Page, base_url: str, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = ViewUrlHelper(
            base_url + "/admin/resource/quotes/",
            "Quotes List Page",
            page,
            user_name=user_name,
        )
        self.user_name = user_name

    quotes_resources_title_desc = "Quotes Resources Title"
    quotes_resources_title_selector = "[test-id='items--title']:has-text('Quotes')"

    @property
    def quotes_resources_title(self):
        return PageSelectorHelper(
            self.page,
            self.quotes_resources_title_selector,
            self.quotes_resources_title_desc,
        )
