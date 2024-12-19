===============================
Setup a local tahoe test server
===============================

Before you begin
================

Create and activate a local venv for tahoe::

    python -m venv .venv && source .venv/bin/activate

Update the new venv and install tahoe-lafs::

    pip install -U pip setuptools wheel && \
    pip install attrs==23.2.0 'cryptography<42' tahoe-lafs

.. note:: Use multiple terminal sessions for each of the various consoles you will eventually start. Most IDE's support independent terminals.


Verify the CLI
--------------

Run ``tahoe --version`` to confirm that the CLI is installed

``tmux`` is your friend
-----------------------

Most Tahoe operators are running Linux in terminal sessions. Using ``tmux`` will make life easier because you will be running several processes, it helps to have multiple terminal windows.
A Linux terminal user would create several sessions like this::

    $ tmux new -s storage_console
    $ tmux new -s client_console


Create a simple storage node
============================

.. note:: Estimated time is 5 minutes

1. Create a simple node to serve as storage server:

.. code-block::

    $ tahoe --node-directory=./storage0 create-node \
     --hostname=localhost \
     --nickname=storage0 \
     --webport=none

.. note:: Ignore the response ``Please add introducers ... The node cannot connect to a grid without it.``

Start the node process
----------------------

Now, in the terminal session you created earlier and called ``storage_console``::

    $ tahoe run storage0

At the end of the console listing, you should see something similar to::

    2024-09-10T12:54:21-0700 [-] client running

Congratulations, you have created a minimal storage node, ready to serve clients.


Create a client node
=====================

.. note:: Estimated time is 15 minutes


To interact with tahoe-lafs services, you need to creat and start a client.

.. note:: Ignore the response ``Please add introducers ... The node cannot connect to a grid without it.``

Create a simple client configuration::

    $ tahoe --node-directory=client0 create-client \
    --shares-happy=1 \
    --shares-needed=1 \
    --shares-total=1 \
    --nickname=client0


You will see the console output end with something like:

.. code-block::console

    2024-09-19T13:31:13-0400 [foolscap.pb.Listener#info] Starting factory <Listener at 0x10f1624e0 on CleanupEndpoint(_wrapped=<twisted.internet.endpoints.AdoptedStreamServerEndpoint object at 0x10f161ca0>, _fd=10, _listened=True) with tub x2hgwovdakx3kdelyetg3duzh4chyt22>
    2024-09-19T13:31:13-0400 [-] client running

Stop the client using Ctrl-C

.. note:: Congratulations! You're now ready to configure your Tahoe client

Prepare the client
===================

Point the client to the storage node
------------------------------------

For now, we will tell the client how to find server, using a static configuration setting.
Create a ``./client0/private/servers.yaml`` file in the client configuration directory::

    $ nano ./client0/private/servers.yaml

.. note:: You may not want to put this file in source control...

At first, the file is empty, when complete, the contents of the file will look something like this::

    storage:
      v0-qacl3os464epv7olvwolv55tqlrimfj2bpwwjo43qfotlwxpfcsa:
        ann:
          nickname: storage0
          anonymous-storage-FURL: pb://wknlsj5cfrfogj7je2gjd2azakyf7amd@tcp:localhost:55316/iv6ilyybouwm4o5mbwhstduupkpyhiof

Configure the client with the storage node info
------------------------------------------------

The value for ``storage:`` open the file ``storage0/node.pubkey`` and copy everything after ``pub-``.

The value for ``anonymous-storage-FURL:`` is the entire content of ``./storage0/private/storage.furl``. This is also called the anonymous :term:`fURL` of the storage server.


.. note::  Static server settings are described at https://tahoe-lafs.readthedocs.io/en/latest/configuration.html#static-server-definitions

Start the client process
-------------------------

In the console window called ``client_node``::

    $ tahoe run client0/

The console output should include something like:
``2024-09-10T13:25:33-0700 [-] TahoeLAFSSite starting on 3456`` and end with ``- client running``

In the console output, you will notice that the client runs two network connections:
    - A web app using a REST API on TCP port 3456
    - A protobuf style client using Foolscap on TCP port 57635


Verify the HTML client
======================

Open the client's web UI at http://localhost:3456

or use ``curl -k  http://localhost:3456``

The landing page should show 1 of 1 storage servers connected, 0 introducers and 0 helpers.
This verifies that the client can run Tahoe requests and that the storage node successfully responds.

.. admonition:: Congratulations on completing Step 2 !
    :class: tip

Connect using the ``tahoe`` CLI
===============================

``tahoe --node-directory=./client0 status``


Connect using the Tahoe RESTful Web API
=======================================

.. warning:: The following material is not yet validated. You have been warned.

curl -d t=json http://localhost:3456/

Create a bare immutable

Obtain a directory capability
-----------------------------

Create a root directory

POST /uri?t=mkdir
curl -T http://localhost:3456/uri?t=mkdir



Upload a test


Create a test file:

``echo "Hello World" >> hello_world.txt``


http://127.0.0.1:3456/uri/URI%3ADIR2%3Adjrdkfawoqihigoett4g6auz6a%3Ajx5mplfpwexnoqff7y5e4zjus4lidm76dcuarpct7cckorh2dpgq/welcome.txt

http://127.0.0.1:3456/uri/URI%3ACHK%3Aime6pvkaxuetdfah2p2f35pe54%3A4btz54xk3tew6nd4y2ojpxj4m6wxjqqlwnztgre6gnjgtucd5r4a%3A3%3A10%3A202

Using a public test grid
========================
TODO: create public test grid