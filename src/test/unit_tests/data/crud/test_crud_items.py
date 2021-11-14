from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.get_resource_item")
def test_crud_get_item(mock_get_resource_item: MagicMock):
    db = MagicMock()
    item_id = 1
    crudItems.get_item(db, item_id)
    mock_get_resource_item.assert_called_once_with(db, ItemModel, item_id)

@patch("data.crud.items.baseCrud.get_resource_items")
def test_crud_get_items(mock_get_resource_items: MagicMock):
    db = MagicMock()
    crudItems.get_items(db)
    mock_get_resource_items.assert_called_once_with(db, ItemModel, skip=0, limit=100)

@patch("data.crud.items.baseCrud.get_resource_items")
def test_crud_get_items_custom(mock_get_resource_items: MagicMock):
    db = MagicMock()
    crudItems.get_items(db, skip=2, limit=50)
    mock_get_resource_items.assert_called_once_with(db, ItemModel, skip=2, limit=50)
