from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.get_object")
def test_crud_get_item(mock_get_object: MagicMock):
    db = MagicMock()
    item_id = 1
    crudItems.get_item(db, item_id)
    mock_get_object.assert_called_once_with(db, ItemModel, item_id)

@patch("data.crud.items.baseCrud.get_all_objects")
def test_crud_get_all_items(mock_get_all_objects: MagicMock):
    db = MagicMock()
    crudItems.get_items(db)
    mock_get_all_objects.assert_called_once_with(db, ItemModel, skip=0, limit=100)

@patch("data.crud.items.baseCrud.get_all_objects")
def test_crud_get_all_items_custom(mock_get_all_objects: MagicMock):
    db = MagicMock()
    crudItems.get_items(db, skip=2, limit=50)
    mock_get_all_objects.assert_called_once_with(db, ItemModel, skip=2, limit=50)
