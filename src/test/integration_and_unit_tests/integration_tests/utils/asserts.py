def assert_response_error_item_not_found(response):
    assert response.json()["detail"] == "Item not found"


def assert_response_error_invalid_login(response):
    assert response.json()["detail"] == "Incorrect login"


def assert_response_error_expired_or_inactive_link(response):
    assert response.json()["detail"] == "Expired or inactive code"


def assert_response_error_resource_not_accessible(response):
    assert response.json()["detail"] == "Not authorized to access this resource"
