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

from gridsync import APP_NAME
from gridsync.log import initialize_logger
from gridsync.network import get_free_port
from gridsync.supervisor import Supervisor
from gridsync.tahoe import Tahoe


port = config('PORT')

print(port)

initialize_logger()


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

