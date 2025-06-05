"""This is the gridsync conftest without most of the magic wormhole/folder fixtures.
Local imports have been rewritten to match the private facts directory structure
"""

import os
import os.path
import sys
from base64 import b64encode
from functools import partial
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_twisted import async_yield_fixture
from decouple import config

# from gridsync import APP_NAME
# from gridsync.log import initialize_logger
# from gridsync.network import get_free_port
# from gridsync.supervisor import Supervisor
from gridsync.tahoe import Tahoe
from gridsync.settings import APP_NAME

# These settings are for the "fake" object. I think

PORT = 3456

if sys.platform == "darwin":
    application_bundle_path = str(
        Path(
            os.getcwd(),
            "dist",
            APP_NAME + ".app",
            "Contents",
            "MacOS",
        ).resolve()
    )
else:
    application_bundle_path = str(
        Path(os.getcwd(), "dist", APP_NAME).resolve()
    )

os.environ["PATH"] = application_bundle_path + os.pathsep + os.environ["PATH"]

@async_yield_fixture(scope="module")
async def tahoe_server(tmp_path_factory):
    server = Tahoe(tmp_path_factory.mktemp("tahoe_server") / "nodedir")
    settings = {
        "port": f"tcp:{PORT}:interface=127.0.0.1",
        "location": f"tcp:127.0.0.1:{PORT}",
    }
    await server.create_node(settings)
    server.config_set("storage", "reserved_space", "10M")
    await server.start()
    yield server
    await server.stop()


@async_yield_fixture(scope="module")
async def tahoe_client(tmp_path_factory, tahoe_server):
    client = Tahoe(tmp_path_factory.mktemp("tahoe_client") / "nodedir")
    settings = {
        "nickname": "Test Grid",
        "shares-needed": "1",
        "shares-happy": "1",
        "shares-total": "1",
        "convergence": "a" * 52,
        "storage": {
            "test-grid-storage-server-1": {
                "nickname": "test-grid-storage-server-1",
                "anonymous-storage-FURL": tahoe_server.storage_furl,
            }
        },
    }
    await client.create_client(settings)
    client.save_settings(settings)
    await client.start()
    yield client
    await client.stop()