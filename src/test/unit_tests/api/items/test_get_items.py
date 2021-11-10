from unittest.mock import MagicMock, patch
import logging

from api.items.routes import get_items

logger = logging.getLogger(__name__)

@patch.object(get_items, "__defaults__", (0, 100, "mock_db",))
@patch("api.items.routes.crudItems.get_items")
def test__routes_get_items__default_query_params(mock_crud_get_items: MagicMock):
    response = get_items()
    mock_crud_get_items.assert_called_once_with("mock_db", skip = 0, limit = 100)
    assert response == mock_crud_get_items()

@patch.object(get_items, "__defaults__", (0, 100, "mock_db",))
@patch("api.items.routes.crudItems.get_items")
def test__routes_get_items__custom_query_params(mock_crud_get_items: MagicMock):
    response = get_items(skip=2, limit=50)
    mock_crud_get_items.assert_called_once_with("mock_db", skip = 2, limit = 50)
    assert response == mock_crud_get_items()
