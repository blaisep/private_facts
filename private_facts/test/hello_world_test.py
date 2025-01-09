import subprocess

def test_hello_world():
    expected = "The contents of the test string are: Hello, world!"
    process = subprocess.run(
        ["python3", "/Users/bpabon/src/repos/tahoe/private_facts/private_facts/src/hello_world/hello_world.py"], capture_output=True, text=True
    )
    output = process.stdout.rstrip()
    assert output == expected
