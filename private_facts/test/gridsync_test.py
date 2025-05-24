# something like uv run python private_facts/src/gridsync/tahoe.py to make sure that all the dependencies are co
import pytest

@pytest.mark.skip(reason="This just exists to make sure we can instantiate the tahoe_server fixture")
def test_tahoe_server_fixture(tahoe_server):
    test_server = tahoe_server
    assert True