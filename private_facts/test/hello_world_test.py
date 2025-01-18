
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


@pytest.mark.skip(reason="Code has changed.")
def test_entrypoint():
    expected = "The contents of the test string are: Hello, world!"
    process = subprocess.run(
        ["python3", "private_facts/src/hello_world/hello_world.py"], capture_output=True, text=True
    )
    output = process.stdout.rstrip()
    assert output == expected

@pytest.mark.skip(reason="Code has changed.")
def test_upload_string_deprecated():
    expected = "http://127.0.0.1:3456/uri/URI%3ADIR2%3Adjrdkfawoqihigoett4g6auz6a%3Ajx5mplfpwexnoqff7y5e4zjus4lidm76dcuarpct7cckorh2dpgq/"
    result = upload_string()
    assert result == expected

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

def test_upload_string(capsys):
    tahoe_client = FakeTahoe()
    result = upload_string(tahoe_client, 'test_string')
    expected = 'test_string_uri'
    output = capsys.readouterr().out.rstrip()
    expected_output = fake_data.get('test_string')

    assert result == expected
    assert output == expected_output

def test_retrieve_string():
    tahoe_client = FakeTahoe()
    result = get_string(tahoe_client, upload_string(tahoe_client, 'test_string'))

    expected = 'test_string'

    assert result == expected
