import logging

from playwright.sync_api import expect, Page
import allure

logger = logging.getLogger(__name__)

class PageSelectorHelper:
    def __init__(self, page: Page, selector: str, selector_desc: str, user_name: str = "Anonymous"):
        self.page = page
        self.selector = selector
        self.selector_desc = selector_desc
        self.user_name = user_name

    def click(self):
        step_desc = f"User '{self.user_name}' click on '{self.selector_desc}'"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).click()
        step_wrapper()

    def type(self, text: str, delay: int = None, timeout: int = None):
        step_desc = f"User '{self.user_name}' type '{text}' on '{self.selector_desc}'"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).type(text, delay=delay, timeout=timeout)
        step_wrapper()

    def expectToBeVisible(self, timeout = None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to be visible"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_be_visible(timeout=timeout)
        step_wrapper()

    def expectNotToBeVisible(self, timeout = None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to not be visible"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).not_to_be_visible(timeout=timeout)
        step_wrapper()

    def expectToHaveValue(self, value: str, timeout = None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to have value"
        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_have_value(value, timeout=timeout)
        step_wrapper()
