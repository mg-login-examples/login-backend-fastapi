import logging

from playwright.sync_api import expect, Page
from playwright._impl._api_structures import Position
import allure  # type: ignore

logger = logging.getLogger(__name__)


class PageSelectorHelper:
    def __init__(
        self,
        page: Page,
        selector: str,
        selector_desc: str,
        user_name: str = "Anonymous",
    ):
        self.page = page
        self.selector = selector
        self.selector_desc = selector_desc
        self.user_name = user_name

    def click(
        self,
        position: Position | None = None,
        delay: int | None = None,
        timeout: int | None = None,
    ):
        step_desc = f"User '{self.user_name}' click on '{self.selector_desc}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).click(
                position=position, delay=delay, timeout=timeout
            )

        step_wrapper()

    def hover(self, position: Position | None = None, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' hover on '{self.selector_desc}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).hover(position=position, timeout=timeout)

        step_wrapper()

    def fill(self, text: str, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' fill '{text}' on '{self.selector_desc}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).fill(text, timeout=timeout)

        step_wrapper()

    def type(self, text: str, delay: int | None = None, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' type '{text}' on '{self.selector_desc}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).type(text, delay=delay, timeout=timeout)

        step_wrapper()

    def clear(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' clear field '{self.selector_desc}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            self.page.locator(self.selector).clear(timeout=timeout)

        step_wrapper()

    def check_if_visible(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' check if visible"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            return self.page.locator(self.selector).is_visible(timeout=timeout)

        return step_wrapper()

    def expect_to_be_visible(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' to be visible"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_be_visible(timeout=timeout)

        step_wrapper()

    def check_if_not_visible(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' check if not visible"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            return self.page.locator(self.selector).is_hidden(timeout=timeout)

        return step_wrapper()

    def expect_not_to_be_visible(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' not to be visible"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).not_to_be_visible(timeout=timeout)

        step_wrapper()

    def check_if_enabled(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' check if enabled"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            return self.page.locator(self.selector).is_enabled(timeout=timeout)

        return step_wrapper()

    def expect_to_be_enabled(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' to be enabled"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_be_enabled(timeout=timeout)

        step_wrapper()

    def check_if_disabled(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' check if disabled"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            return self.page.locator(self.selector).is_disabled(timeout=timeout)

        return step_wrapper()

    def expect_to_be_disabled(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' to be disabled"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_be_disabled(timeout=timeout)

        step_wrapper()

    def check_if_checked(self, timeout: int | None = None):
        step_desc = f"User '{self.user_name}' check if checked"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            return self.page.locator(self.selector).is_checked(timeout=timeout)

        return step_wrapper()

    def expect_to_be_checked(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' to be checked"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_be_checked(timeout=timeout)

        step_wrapper()

    def expect_not_to_be_checked(self, timeout=None):
        step_desc = (
            f"User '{self.user_name}' expect '{self.selector_desc}' not to be checked"
        )

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).not_to_be_checked(timeout=timeout)

        step_wrapper()

    def expect_to_have_text(self, text: str, timeout=None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to have text '{text}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_have_text(text, timeout=timeout)

        step_wrapper()

    def expect_to_contain_text(self, text: str, timeout=None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to contain text '{text}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_contain_text(
                text, timeout=timeout
            )

        step_wrapper()

    def expect_to_have_value(self, text: str, timeout=None):
        step_desc = f"User '{self.user_name}' expect '{self.selector_desc}' to have value '{text}'"

        @allure.step(step_desc)
        def step_wrapper():
            logger.info(step_desc)
            expect(self.page.locator(self.selector)).to_have_value(
                text, timeout=timeout
            )

        step_wrapper()
