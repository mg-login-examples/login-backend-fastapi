from unittest.mock import MagicMock, patch

from app_factory import create_app

@patch("app_factory.add_cors")
@patch("app_factory.FastAPI")
def test__create_app(mock_FastAPI: MagicMock, mock_add_cors: MagicMock):
    app = create_app()
    mock_add_cors.assert_called()
    mock_FastAPI.assert_called()
    assert app == mock_FastAPI()
