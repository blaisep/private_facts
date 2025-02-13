======================
Joining a storage Grid
======================

.. this is also be added to expand the tutorial in the upstream Tahoe-lafs.


What is the public test grid?
=============================

There is a test grid for temporary storage, as a community service.
It is intended to provide an easy way to play with Tahoe without having to run and configure your own server.
Use at your risk, it is a public lab after all.Do not store sensitive data

This repo includes some static configuration files in the ``tahoe-server/pub-grid/`` directory, so that you can get through
the exercises easily.
Use that static configuration, for learning purposes only because the keys are not private. Later in this tutorial,
you will learn to configure your client and then you should always use your own settings.


Why use a grid?
===============

A grid provides redundant storage by storing your data across multiple storage servers.

When Do you need a grid?
========================

Possibly redundant with "Why use a grid" above?

Connect to the public test grid
===============================

To connect to the public test grid we need to know its introducer fURL.
This is a short URI-like string that would normally remain constant, but
can sometimes change for the test grid since testing and re-deployment is
part of what it's for.

Find the current introducer fURL for the public test grid at the
`PubGrid wiki page <https://tahoe-lafs.org/trac/tahoe-lafs/wiki/TestGrid#HowToConnectToThePublicTestGrid>`_.

.. instructions for the public test grid...

To connect to the grid, we have to set up a client node

.. code-block:: console

    $ tahoe create-client \
    --nickname=pubgrid \
    --basedir=pubgrid-client \
    --introducer=pb://flm2vcjxaxoyah3f2ufdk74augada55i@tcp:testgrid.tahoe-lafs.org:5000/s3kbdgg3j4ohifa633tt7yi25drl6jqa \
    --webport=tcp:3457:interface=127.0.0.1 \
    --shares-happy=3 \
    --shares-needed=2 \
    --shares-total=3

    $ tahoe run pubgrid-client
