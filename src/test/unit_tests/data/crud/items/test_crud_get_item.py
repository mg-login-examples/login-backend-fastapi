from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel

@patch("data.crud.items.baseCrud.get_resource_item")
def test__crud_get_item__calls__baseCrud_get_resource_item(mock_get_resource_item: MagicMock):
    db = MagicMock()
    item_id = 1
    crudItems.get_item(db, item_id)
    mock_get_resource_item.assert_called_once_with(db, ItemModel, item_id)

@patch("data.crud.items.baseCrud.get_resource_item")
def test__crud_get_item__returns__item(mock_get_resource_item: MagicMock):
    db = MagicMock()
    item_id = 1
    mock_get_resource_item.return_value = ItemModel(id=item_id)
    response = crudItems.get_item(db, item_id)
    assert response.id == item_id
