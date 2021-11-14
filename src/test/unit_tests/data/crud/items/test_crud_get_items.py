from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.get_resource_items")
def test__crud_get_items__calls__baseCrud_get_resource_items(mock_get_resource_items: MagicMock):
    db = MagicMock()
    crudItems.get_items(db)
    mock_get_resource_items.assert_called_once_with(db, ItemModel, skip=0, limit=100)

@patch("data.crud.items.baseCrud.get_resource_items")
def test__crud_get_items_with_params__calls__baseCrud_get_resource_items(mock_get_resource_items: MagicMock):
    db = MagicMock()
    crudItems.get_items(db, skip=2, limit=50)
    mock_get_resource_items.assert_called_once_with(db, ItemModel, skip=2, limit=50)

@patch("data.crud.items.baseCrud.get_resource_items")
def test__crud_get_items__returns__list_of_item(mock_get_resource_items: MagicMock):
    db = MagicMock()
    mock_get_resource_items.return_value = [ItemModel()]
    items = crudItems.get_items(db)
    for item in items:
        assert(isinstance(item, ItemModel))
