
import pytest
import subprocess
from hello_world import upload_string, get_string

# The key is the data to be uploaded; the value is the URI Tahoe returns.
fake_data = {
    'test_string': 'test_string_uri'
}

class FakeTahoe:
    """
    An object which mocks a Tahoe client.
    """
    def __init__(self, storage={}):
        self.storage = storage

    def upload_data(self, data):
        uri = fake_data.get(data) # Get the URI from the fake_data dict
        self.storage[uri] = data # Store the URI as key and the data as value for later retrieval
        return uri

    def retrieve_data(self, uri):
        return self.storage.get(uri)

# FakeTahoe tests
def test_fake_tahoe_upload_string():
    fake_tahoe = FakeTahoe()
    result = fake_tahoe.upload_data('test_string')
    expected = fake_data.get('test_string')
    
    assert result == expected

def test_fake_tahoe_upload_and_retrieve_string():
    fake_tahoe = FakeTahoe()
    uri = fake_tahoe.upload_data('test_string')
    result = fake_tahoe.retrieve_data(uri)
    expected = 'test_string'
    
    assert result == expected

# hello_world tests
def test_upload_string(capsys):
    tahoe_client = FakeTahoe()
    result = upload_string(tahoe_client, 'test_string')
    expected = 'test_string_uri'
    output = capsys.readouterr().out.rstrip()
    expected_output = fake_data.get('test_string')

    assert result == expected
    assert output == expected_output

def test_get_string(capsys):
    tahoe_client = FakeTahoe()
    result = get_string(tahoe_client, upload_string(tahoe_client, 'test_string'))
    expected = 'test_string'
    output = capsys.readouterr().out.rstrip().split()[1] # Get only the second line of output, since upload_string also prints a line
    expected_output = expected

    assert result == expected
    assert output == expected_output