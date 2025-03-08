import pytest
from unittest.mock import Mock
from hello.tahoe_client import TahoeClient

BASE_URL="http://127.0.0.1:3456/"

@pytest.fixture
def mock_http():
    return Mock()

@pytest.fixture
def client(mock_http):
    return TahoeClient(base_url=BASE_URL, http=mock_http)

@pytest.fixture
def client_dircap(mock_http):
    return TahoeClient(base_url=BASE_URL, http=mock_http, dir_cap="$DIRCAP")

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
def test_upload_data_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"cap_string")
    mock_http.request.return_value = mock_response

    result = client.upload_data("test data")

    mock_http.request.assert_called_once_with("PUT", "http://127.0.0.1:3456/", "test data")
    assert result == "cap_string"

def test_upload_data_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response
    
    result = client.upload_data("test data")

    mock_http.request.assert_called_once_with("PUT", "http://127.0.0.1:3456/", "test data")
    assert result is None

def test_upload_data_exception(client, mock_http):
    mock_http.request.side_effect = Exception()
    
    with pytest.raises(Exception):
        client.upload_data("test data")



# Retrieve data tests
def test_retrieve_data_happy(client, mock_http):
    mock_response = Mock(status=200, data=b"test data")
    mock_http.request.return_value = mock_response

    result = client.retrieve_data("cap_string")

    mock_http.request.assert_called_once_with("GET", "http://127.0.0.1:3456/cap_string")
    assert result[0] == "test data"
    assert result[1] == 200

def test_retrieve_data_bad_response(client, mock_http):
    mock_response = Mock(status=404)
    mock_http.request.return_value = mock_response

    result = client.retrieve_data("cap_string")

    mock_http.request.assert_called_once_with("GET", "http://127.0.0.1:3456/cap_string")
    assert result[0] is None
    assert result[1] == 404


# Make dir tests

# Get welcome tests