import logging
from typing import List

import requests
import pytest

from admin.api.resources import resourcesConfigurations
from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users_admin import created_user_by_admin, created_n_users_by_admin, generate_random_user_to_create
from test.integration_tests.fixtures.dbutils import setup_db
from test.integration_tests.utils import asserts


logger = logging.getLogger(__name__)

# Test that resources can be fetched
def test_get_resources(test_client: requests.Session):
    response = test_client.get(f"/api/admin/resources/")
    assert response.status_code == 200
    responseResourceConfigurationsByResourceUrlId = {configurations["resourceUrlId"] : configurations for configurations in  response.json()}
    for resourceConfigurations in resourcesConfigurations:
        responseResourceConfigurations = responseResourceConfigurationsByResourceUrlId[resourceConfigurations.resource_endpoints_url_prefix]
        assert responseResourceConfigurations["resourceName"]
