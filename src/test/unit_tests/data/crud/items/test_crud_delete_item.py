from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.delete_object")
def test__crud_delete_items__calls__baseCrud_delete_object(mock_delete_object: MagicMock):
    db = MagicMock()
    item_id = 1
    crudItems.delete_item(db, item_id)
    mock_delete_object.assert_called_once_with(db, ItemModel, item_id)

@patch("data.crud.items.baseCrud.delete_object")
def test__crud_delete_items__returns__none(mock_delete_object: MagicMock):
    mock_delete_object.return_value = None
    db = MagicMock()
    item_id = 1
    response = crudItems.delete_item(db, item_id)
    assert response == None
