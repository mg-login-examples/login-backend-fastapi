from unittest.mock import MagicMock, patch

from api.items.routes import create_item


mock_item_to_create = MagicMock()

@patch.object(create_item, "__defaults__", (mock_item_to_create, "mock_db",))
@patch("api.items.routes.crudItems.create_item")
def test__routes_get_items__default_query_params(mock_crud_create_item: MagicMock):
    response = create_item()
    mock_crud_create_item.assert_called_once_with("mock_db", mock_item_to_create)
    assert response == mock_crud_create_item()
