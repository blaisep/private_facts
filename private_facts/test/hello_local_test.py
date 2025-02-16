import pytest
import subprocess
from hello.hello_local import upload_string, get_string

# The key is the data to be uploaded; the value is the URI Tahoe returns.
fake_data = {
    'test_string': 'test_string_uri'
}

class FakeTahoe:
    """
    An object which mocks a Tahoe client.
    """
    def __init__(self, storage={}, bad_response=False):
        self.storage = storage
        self.bad_response = bad_response

    def upload_data(self, data, exception=False):
        if exception:
            raise ValueError("Simulated exception.")
        if self.bad_response:
            return None
        uri = fake_data.get(data) # Get the URI from the fake_data dict
        self.storage[uri] = data # Store the URI as key and the data as value for later retrieval
        return uri

    def retrieve_data(self, uri):
        if self.bad_response:
            status = 400
            return None, status
        status = 200
        return self.storage.get(uri), status

# FakeTahoe tests
def test_fake_tahoe_upload_string_happy():
    fake_tahoe = FakeTahoe()
    result = fake_tahoe.upload_data('test_string')
    expected = fake_data.get('test_string')
    
    assert result == expected

def test_fake_tahoe_upload_string_exception():
    fake_tahoe = FakeTahoe()
    with pytest.raises(ValueError) as e:
        fake_tahoe.upload_data('test_string', exception=True)
    assert str(e.value) == 'Simulated exception.'

def test_fake_tahoe_upload_string_bad_response():
    fake_tahoe = FakeTahoe(bad_response=True)
    result = fake_tahoe.upload_data('test_string')

    assert result is None

def test_fake_Tahoe_retrieve_string():
    fake_tahoe = FakeTahoe()
    uri = fake_data.get('test_string')
    result, status = fake_tahoe.retrieve_data(uri)
    expected = 'test_string'
    expected_status = 200

    assert result == expected
    assert status == expected_status

def test_fake_tahoe_retrieve_string_bad_response():
    fake_tahoe = FakeTahoe(bad_response=True)
    uri = fake_data.get('test_string')
    result, status = fake_tahoe.retrieve_data(uri)

    assert result is None
    assert status == 400


def test_fake_tahoe_upload_and_retrieve_string():
    fake_tahoe = FakeTahoe()
    uri = fake_tahoe.upload_data('test_string')
    result, status = fake_tahoe.retrieve_data(uri)
    expected = 'test_string'
    expected_status = 200
    
    assert result == expected
    assert status == expected_status

# hello_local tests
def test_upload_string_happy(capsys):
    tahoe_client = FakeTahoe()
    result = upload_string(tahoe_client, 'test_string')
    expected = 'test_string_uri'
    output = capsys.readouterr().out.rstrip()
    expected_output = fake_data.get('test_string')

    assert result == expected
    assert output == expected_output

def test_upload_string_bad_response(capsys):
    tahoe_client = FakeTahoe(bad_response=True)
    result = upload_string(tahoe_client, 'test_string')
    output = capsys.readouterr().out.rstrip()
    expected_output = "An error occurred during upload."

    assert result is None
    assert output == expected_output

def test_get_string(capsys):
    tahoe_client = FakeTahoe()
    result = get_string(tahoe_client, upload_string(tahoe_client, 'test_string'))
    expected = 'test_string'
    output = capsys.readouterr().out.rstrip().split()[1] # Get only the second output, since upload_string also prints a line
    expected_output = expected

    assert result == expected
    assert output == expected_output

def test_get_string_bad_response(capsys):
    tahoe_client = FakeTahoe(bad_response=True)
    result = get_string(tahoe_client, upload_string(tahoe_client, 'test_string'))
    output = capsys.readouterr().out.rstrip().split('\n')[1] # Get only the second line of output, since upload_string also prints a line
    expected_output = "An error occurred retrieving the data with error code: 400"

    assert output == expected_output
    assert result is None