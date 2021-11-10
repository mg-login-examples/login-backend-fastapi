from unittest.mock import MagicMock, patch

from settings.cors_settings import add_cors

@patch("settings.cors_settings.CORSMiddleware")
def test__add_cors(mock_CORSMiddleware: MagicMock):
    mock_app = MagicMock()
    add_cors(mock_app)
    mock_app.add_middleware.assert_called_with(
        mock_CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
