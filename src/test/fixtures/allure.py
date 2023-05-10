import os
import glob
import pytest
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session', autouse=True)
def clean_allure_results():
    logger.debug("Create fixture clean_allure_results")
    # Delete all files inside the allure-results before a test run
    files = glob.glob('allure-results/*')
    for f in files:
        os.remove(f)
