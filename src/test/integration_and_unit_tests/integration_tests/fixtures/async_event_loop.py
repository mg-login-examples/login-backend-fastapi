import asyncio
import logging
import pytest

logger = logging.getLogger(__name__)

@pytest.fixture
def event_loop():
    logger.debug("Create fixture event_loop")
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()