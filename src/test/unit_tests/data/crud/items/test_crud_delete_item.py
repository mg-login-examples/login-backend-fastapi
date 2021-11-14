from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.delete_resource_item")
def test__crud_delete_items__calls__baseCrud_delete_resource_item(mock_delete_resource_item: MagicMock):
    db = MagicMock()
    item_id = 1
    crudItems.delete_item(db, item_id)
    mock_delete_resource_item.assert_called_once_with(db, ItemModel, item_id)
