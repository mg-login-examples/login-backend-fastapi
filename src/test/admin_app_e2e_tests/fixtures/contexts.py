import logging

import pytest
from playwright.sync_api._generated import Browser

logger = logging.getLogger(__name__)


@pytest.fixture
def my_playwright_context(browser: Browser):
    context = browser.new_context()
    yield context
    logger.info("start closing browser context")
    context.close()
    logger.info("end closing browser context")
