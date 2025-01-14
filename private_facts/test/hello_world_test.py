
import pytest
import subprocess
from hello_world import upload_string


@pytest.mark.skip(reason="Code has changed.")
def test_entrypoint():
    expected = "The contents of the test string are: Hello, world!"
    process = subprocess.run(
        ["python3", "private_facts/src/hello_world/hello_world.py"], capture_output=True, text=True
    )
    output = process.stdout.rstrip()
    assert output == expected

@pytest.mark.skip(reason="Code has changed.")
def test_upload_string():
    expected = "http://127.0.0.1:3456/uri/URI%3ADIR2%3Adjrdkfawoqihigoett4g6auz6a%3Ajx5mplfpwexnoqff7y5e4zjus4lidm76dcuarpct7cckorh2dpgq/"
    result = upload_string()
    assert result == expected