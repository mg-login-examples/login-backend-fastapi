import logging

from playwright.sync_api import expect, Page
import allure

logger = logging.getLogger(__name__)


class ViewUrlHelper:
    def __init__(self, view_url: str, view_name: str,
                 page: Page, user_name: str = "Anonymous"):
        self.page = page
        self.view_url = view_url
        self.view_name = view_name
        self.user_name = user_name

    def try_to_open(self):
        step_desc = f"User '{self.user_name}' try to open {
            self.view_name} with url '{self.view_url}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.goto(self.view_url)
        step_wrapper()

    def expect_to_be_open(self):
        step_desc = f"User '{self.user_name}' expect {
            self.view_name} is open with url '{self.view_url}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page).to_have_url(self.view_url)
        step_wrapper()

    def open(self):
        step_desc = f"User '{self.user_name}' open {
            self.view_name} with url '{self.view_url}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.try_to_open()
            self.expect_to_be_open()
        step_wrapper()
