from unittest.mock import MagicMock, patch

from data.crud import items as crudItems
from data.database.models.item import Item as ItemModel
from data.schemas.items import ItemCreate as ItemCreateSchema

@patch("data.crud.items.ItemModel")
@patch("data.crud.items.baseCrud.create_object")
def test__crud_create_item__calls__baseCrud_create_object(mock_create_object: MagicMock, mock_ItemModel: MagicMock):
    db = MagicMock()
    item_to_create = MagicMock()
    item_to_create_as_model = MagicMock()
    mock_ItemModel.return_value = item_to_create_as_model

    crudItems.create_item(db, item_to_create)

    mock_create_object.assert_called_once_with(db, item_to_create_as_model)

@patch("data.crud.items.baseCrud.create_object")
def test__crud_create_item__returns__created_item(mock_create_object: MagicMock):
    db = MagicMock()
    item_to_create = ItemCreateSchema(name="test_name", description="test_description")
    mock_create_object.side_effect = lambda db, item_as_model: item_as_model

    item_created = crudItems.create_item(db, item_to_create)

    assert item_created.name == item_to_create.name
    assert item_created.description == item_to_create.description
