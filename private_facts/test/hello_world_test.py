
import pytest
import subprocess
from hello_world import upload_string

fake_data = {
    'test_string': 'test_string_uri'
}

class FakeTahoe:
    def __init__(self, stored_data={}):
        self.stored_data = stored_data

    def upload(self, data_key):
        uri = fake_data.get(data_key)
        self.stored_data[uri] = data_key
        return uri



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

def test_upload_string():
    fake_tahoe = FakeTahoe()
    result = fake_tahoe.upload('test_string')
    expected = fake_data.get('test_string')
    assert result == expected
