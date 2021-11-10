from unittest.mock import MagicMock, patch

from data.database.dbUtils import create_all_tables

@patch("data.database.dbUtils.BaseModel.metadata.create_all")
def test_create_all_tables(mock_from_BaseModel_create_all_models: MagicMock):
    mock_engine = MagicMock()
    create_all_tables(mock_engine)
    mock_from_BaseModel_create_all_models.assert_called_once_with(bind=mock_engine)
