import os
import pytest
from unittest.mock import patch, mock_open, MagicMock

import requests

from superfaktura.superfaktura_api import (
    SuperFakturaAPI,
    SuperFakturaAPIException,
    SuperFakturaAPIMissingCredentialsException,
)

@pytest.fixture
def api():
    with patch.dict(os.environ, {
        "SUPERFAKTURA_API_KEY": "test_key",
        "SUPERFAKTURA_API_URL": "https://api.superfaktura.cz",
        "SUPERFAKTURA_API_EMAIL": "test_email",
        "SUPERFAKTURA_API_COMPANY_ID": "test_company_id"
    }):
        return SuperFakturaAPI()

def test_missing_credentials():
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(SuperFakturaAPIMissingCredentialsException):
            SuperFakturaAPI()

def test_get(api):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"data": "test"}
        response = api.get("test_endpoint")
        assert response == {"data": "test"}

def test_get_failure(api):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        with pytest.raises(SuperFakturaAPIException):
            api.get("test_endpoint")

def test_download(api):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"test_content"
        with patch("builtins.open", mock_open()) as mock_file:
            with open("test_file", "wb") as f:
                api.download("test_endpoint", f)
            mock_file().write.assert_called_once_with(b"test_content")

def test_download_failure(api):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        with patch("builtins.open", mock_open()):
            with open("test_file", "wb") as f:
                with pytest.raises(SuperFakturaAPIException):
                    api.download("test_endpoint", f)

def test_post(api):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"data": "test"}
        response = api.post("test_endpoint", '{"name": "Example"}')
        assert response == {"data": "test"}

def test_post_failure(api):
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 404
        mock_post.return_value.json.return_value = {"error": "not found"}
        with pytest.raises(SuperFakturaAPIException):
            api.post("test_endpoint", '{"name": "Example"}')

def test_get_invalid_json(api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("msg", "doc", 0)
        mock_get.return_value = mock_response
        with pytest.raises(SuperFakturaAPIException, match="Unable to decode response as JSON"):
            api.get("test_endpoint")

def test_download_not_writable_descriptor(api):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"test_content"
        mock_descriptor = MagicMock()
        mock_descriptor.writable.return_value = False
        with patch("builtins.open", mock_open()) as mock_file:
            with pytest.raises(SuperFakturaAPIException, match=" is not writable"):
                api.download("test_endpoint", mock_descriptor)
