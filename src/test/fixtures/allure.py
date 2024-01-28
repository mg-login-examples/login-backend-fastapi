import os
import glob
import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session', autouse=True)
def clean_allure_results():
    logger.info("Create fixture clean_allure_results")
    # Delete all files inside the allure-results before a test run
    files = glob.glob('test/allure-results/*')
    for f in files:
        try:
            os.remove(f)
        except Exception as e:
            logger.debug("Error while deleting allure results files:")
            logger.debug(e)
