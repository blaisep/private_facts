import pytest

@pytest.mark.skip(reason="Doesn't work")
def test_fixtures(tahoe_server, tahoe_client):
    test_server = tahoe_server
    test_client = tahoe_client(test_server)
    assert True