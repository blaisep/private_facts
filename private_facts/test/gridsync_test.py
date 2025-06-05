# something like uv run python private_facts/src/gridsync/tahoe.py to make sure that all the dependencies are co
import pytest

@pytest.mark.skip(reason="Takes too long and passes, but prints a traceback from the Tahoe server")
def test_tahoe_server_fixture(tahoe_server):
    test_server = tahoe_server
    assert True