import logging

from playwright.sync_api import Page
import allure  # type: ignore

logger = logging.getLogger(__name__)


def save_screenshot(page: Page, screenshot_name: str):
    try:
        screenshot = page.screenshot(full_page=True)
        allure.attach(screenshot, name=screenshot_name,
                      attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logger.error("Error while taking screenshot and attaching to allure:")
        logger.error(e)
