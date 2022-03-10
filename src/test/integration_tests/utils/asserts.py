
def assert_response_error_item_not_found(response):
    assert response.json()['detail'] == 'Item not found'
