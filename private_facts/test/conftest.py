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
from private_facts.src.gridsync.tahoe import Tahoe

# These settings are for the "fake" object. I think

PORT = 3456

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

# @async_yield_fixture(scope="module")
# async def zkapauthorizer(tmp_path_factory, tahoe_server):
#     from gridsync.zkapauthorizer import PLUGIN_NAME

#     client = Tahoe(tmp_path_factory.mktemp("tahoe_client") / "nodedir")
#     settings = {
#         "nickname": "ZKAPAuthorizer-enabled Test Grid",
#         "shares-needed": "1",
#         "shares-happy": "1",
#         "shares-total": "1",
#         "storage": {
#             "test-grid-storage-server-1": {
#                 "anonymous-storage-FURL": "pb://@tcp:/",
#                 "nickname": "test-grid-storage-server-1",
#                 "storage-options": [
#                     {
#                         "name": PLUGIN_NAME,
#                         "ristretto-issuer-root-url": "https://example.org/",
#                         "storage-server-FURL": tahoe_server.storage_furl,
#                         "allowed-public-keys": "AAAAAAAAAAAAAAAA",
#                     }
#                 ],
#             }
#         },
#     }
#     await client.create_client(settings)
#     client.save_settings(settings)
#     await client.start()
#     yield client.zkapauthorizer
#     await client.stop()


@pytest.fixture()
def reactor():
    return Mock()


def _tahoe(tmpdir_factory, reactor):
    client = Tahoe(
        str(tmpdir_factory.mktemp("tahoe")),
        executable="tahoe_exe",
        reactor=reactor,
    )
    with open(os.path.join(client.nodedir, "tahoe.cfg"), "w") as f:
        f.write("[node]\nnickname = default")
    with open(os.path.join(client.nodedir, "icon.url"), "w") as f:
        f.write("test_url")
    private_dir = os.path.join(client.nodedir, "private")
    os.mkdir(private_dir)
    with open(os.path.join(private_dir, "aliases"), "w") as f:
        f.write("test_alias: test_cap")
    with open(os.path.join(private_dir, "magic_folders.yaml"), "w") as f:
        f.write("magic-folders:\n  test_folder: {directory: test_dir}")
    client.set_nodeurl("http://example.invalid:12345/")
    with open(os.path.join(client.nodedir, "node.url"), "w") as f:
        f.write("http://example.invalid:12345/")
    api_token = b64encode(b"a" * 32).decode("ascii")
    client.api_token = api_token
    with open(os.path.join(private_dir, "api_auth_token"), "w") as f:
        f.write(api_token)
    Path(private_dir, "rootcap").write_text(
        "URI:DIR2:x6ciqn3dbnkslpvazwz6z7ic2q:"
        "slkf7invl5apcabpyztxazkcufmptsclx7m3rn6hhiyuiz2hvu6a"
    )
    client.magic_folder = DummyMagicFolder()  # XXX
    return client

class DummyMagicFolder:
    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass


@pytest.fixture()
def tahoe_factory(tmpdir_factory):
    return partial(_tahoe, tmpdir_factory)


@pytest.fixture()
def tahoe(tmpdir_factory, reactor):
    return _tahoe(tmpdir_factory, reactor)


@pytest.fixture()
def fake_tahoe():
    t = Mock()
    t.name = "TestGrid"
    t.shares_happy = 3
    t.settings = {"zkap_payment_url_root": "https://example.invalid./"}
    t.zkapauthorizer = Mock()
    t.zkapauthorizer.zkap_unit_multiplier = 0.001
    t.zkapauthorizer.zkap_unit_name = "MB"
    t.zkapauthorizer.zkap_batch_size = 10000
    return t