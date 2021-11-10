import pytest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from api.items.routes import get_item


@patch.object(get_item, "__defaults__", (1, "mock_db",))
@patch("api.items.routes.crudItems.get_item")
def test__routes_get_item__valid_id(mock_crud_get_item: MagicMock):
    response = get_item()
    mock_crud_get_item.assert_called_once_with("mock_db", 1)
    assert response == mock_crud_get_item()


@patch.object(get_item, "__defaults__", (3, "mock_db",))
@patch("api.items.routes.crudItems.get_item")
def test__routes_get_item__invalid_id(mock_crud_get_item: MagicMock):
    mock_crud_get_item.return_value = None
    with pytest.raises(HTTPException):
        get_item()
    mock_crud_get_item.assert_called_once_with("mock_db", 3)
