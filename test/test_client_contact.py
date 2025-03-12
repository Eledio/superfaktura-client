import os

import pytest  # type: ignore
from unittest.mock import patch
from superfaktura.client_contacts import (
    ClientContactModel,
    ClientContact,
    ClientException,
)


@pytest.fixture
def client_contact():
    with patch.dict(
        os.environ,
        {
            "SUPERFAKTURA_API_KEY": "test_key",
            "SUPERFAKTURA_API_URL": "https://api.superfaktura.cz",
            "SUPERFAKTURA_API_EMAIL": "test_email",
            "SUPERFAKTURA_API_COMPANY_ID": "test_company_id",
        },
    ):
        with patch("superfaktura.client_contacts.ClientContact", return_value=None):
            return ClientContact()


def test_add_contact_success(client_contact):
    client = ClientContactModel(
        name="John Doe",
    )

    with patch("superfaktura.superfaktura_api.SuperFakturaAPI.post") as mock_post:
        mock_post.return_value = {"error_message": "Client created"}
        assert client_contact.add_contact(contact=client)


def test_add_contact_failed(client_contact):
    client = ClientContactModel(
        name="John Doe",
    )

    with patch("superfaktura.superfaktura_api.SuperFakturaAPI.post") as mock_post:
        mock_post.return_value = {"error_message": "Client creation failed"}
        assert not client_contact.add_contact(contact=client)


def test_list(client_contact):
    with patch("superfaktura.superfaktura_api.SuperFakturaAPI.get") as mock_get:
        mock_get.return_value = {"data": "test"}
        assert client_contact.list() == {"data": "test"}


def test_get_client_exists(client_contact):
    with patch("superfaktura.superfaktura_api.SuperFakturaAPI.get") as mock_get:
        mock_get.return_value = {"Client": {"name": "John Doe", "id": 1}}
        assert client_contact.get_client(client_id=1).name == "John Doe"


def test_get_client_not_exists(client_contact):
    with patch("superfaktura.superfaktura_api.SuperFakturaAPI.get") as mock_get:
        mock_get.return_value = {}
        with pytest.raises(ClientException):
            client_contact.get_client(client_id=1)
