from unittest.mock import MagicMock, patch

from api.items.routes import delete_item


@patch.object(delete_item, "__defaults__", (5, "mock_db",))
@patch("api.items.routes.crudItems.delete_item")
def test__routes_get_items__default_query_params(mock_crud_delete_item: MagicMock):
    delete_item()
    mock_crud_delete_item.assert_called_once_with("mock_db", 5)
