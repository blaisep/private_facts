import pytest
from unittest.mock import MagicMock
from hello.tahoe_client import TahoeClient

BASE_URL="http://127.0.0.1:3456"

@pytest.fixture
def mock_http():
    return MagicMock()

@pytest.fixture
def client(mock_http):
    return TahoeClient(base_url=BASE_URL, http=mock_http)

# Client creation tests
def test_create_client_happy(client, mock_http):
    assert client.base_url == BASE_URL
    assert client.http is mock_http
    
def test_create_client_no_url(mock_http):
    with pytest.raises(TypeError) as e:
        client = TahoeClient(mock_http)
    
    error_message = str(e.value)

    assert "missing 1 required positional argument" in error_message
    assert "http" in error_message

def test_create_client_no_http():
    with pytest.raises(TypeError) as e:
        client = TahoeClient(BASE_URL)
    
    error_message = str(e.value)

    assert "missing 1 required positional argument" in error_message
    assert "http" in error_message
    
# Upload data tests

# Retrieve data tests

# Make dir tests

# Get welcome tests