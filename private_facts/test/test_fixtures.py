import pytest
import os
import sys
from pathlib import Path

from gridsync import APP_NAME

if sys.platform == "darwin":
    application_bundle_path = str(
        Path(
            os.getcwd(),
            "dist",
            APP_NAME + ".app",
            "Contents",
            "MacOS",
            "Tahoe-LAFS",
        ).resolve()
    )
else:
    application_bundle_path = str(
        Path(os.getcwd(), "dist", APP_NAME, "Tahoe-LAFS").resolve()
    )

os.environ["PATH"] = application_bundle_path + os.pathsep + os.environ["PATH"]

@pytest.mark.skip(reason="Doesn't work")
def test_fixtures(tahoe_server, tahoe_client):
    test_server = tahoe_server
    test_client = tahoe_client(test_server)
    assert True

def test_tahoe_start_creates_pidfile(tahoe_client):
    assert Path(tahoe_client.pidfile).exists() is True