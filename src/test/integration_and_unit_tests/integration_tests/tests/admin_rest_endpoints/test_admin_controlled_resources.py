import logging

import requests  # type: ignore

from rest_endpoints.admin.resources import resources_configurations

logger = logging.getLogger(__name__)

# Test that resources can be fetched


def test_get_resources(test_client_admin_logged_in: requests.Session):
    response = test_client_admin_logged_in.get(f"/api/admin/resources/")
    assert response.status_code == 200
    responseResourceConfigurationsByResourceUrlId = {
        configurations["resourceUrlId"]: configurations for configurations in response.json()}
    for resource_configuration in resources_configurations:
        responseResourceConfigurations = responseResourceConfigurationsByResourceUrlId[
            resource_configuration.resource_endpoints_url_prefix]
        assert responseResourceConfigurations["resourceName"]
