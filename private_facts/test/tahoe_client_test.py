import pytest
from unittest.mock import MagicMock
from hello.tahoe_client import TahoeClient

@pytest.fixture
def mock_http():
    return MagicMock()

@pytest.fixture
def client(mock_http):
    return TahoeClient(base_url="http://127.0.0.1:3456", http=mock_http)

# Client creation tests
def test_create_client():
    pass

def test_create_client_no_url():
    pass

def test_create_client_no_http():
    pass

# Upload data tests

# Retrieve data tests

# Make dir tests

# Get welcome tests