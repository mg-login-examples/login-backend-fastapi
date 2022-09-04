import logging

import requests

from api.admin.resources import resourcesConfigurations

logger = logging.getLogger(__name__)

# Test that resources can be fetched
def test_get_resources(test_client_admin_logged_in: requests.Session):
    response = test_client_admin_logged_in.get(f"/api/admin/resources/")
    assert response.status_code == 200
    responseResourceConfigurationsByResourceUrlId = {configurations["resourceUrlId"] : configurations for configurations in  response.json()}
    for resourceConfigurations in resourcesConfigurations:
        responseResourceConfigurations = responseResourceConfigurationsByResourceUrlId[resourceConfigurations.resource_endpoints_url_prefix]
        assert responseResourceConfigurations["resourceName"]
