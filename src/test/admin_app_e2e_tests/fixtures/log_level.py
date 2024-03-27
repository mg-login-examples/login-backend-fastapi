import logging
import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def set_logging_level():
    logging.basicConfig(level="DEBUG")
