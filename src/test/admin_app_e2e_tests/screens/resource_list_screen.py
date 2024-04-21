from test.admin_app_e2e_tests.utils.page_selector_helper import PageSelectorHelper

from playwright.sync_api import Page


class ResourceListViewScreen:
    def __init__(self, page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.user_name = user_name

    navigate_to_last_page_button_desc = "Navigate To Last Page Button"
    navigate_to_last_page_button_selector = "[test-id='items--last-items-button']"

    @property
    def navigate_to_last_page_button(self):
        return PageSelectorHelper(
            self.page,
            self.navigate_to_last_page_button_selector,
            self.navigate_to_last_page_button_desc,
        )

    create_new_item_button_desc = "Create New Item Button"
    create_new_item_button_selector = "[test-id='resource-items--add-item-button']"

    @property
    def create_new_item_button(self):
        return PageSelectorHelper(
            self.page,
            self.create_new_item_button_selector,
            self.create_new_item_button_desc,
        )
