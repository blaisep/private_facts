Using the Sample App Tutorial
=============================

Learn to integrate Tahoe-LAFS with your app using the Web API, let's start by interacting with the service using the CLI.

Ensure your client is working
------------------------------

Use the CLI to move some files in and out of Tahoe-LAFS

Upload a simple text file
--------------------------

.. tab:: CLI

    .. code-block:: bash

        $ echo "Hello Tahoe" > hello.txt
        $ tahoe --node-directory=tahoe-server/client0 put ./hello.txt

.. tab:: Python

    .. code-block:: python

        Python example

.. tab:: Curl

    .. code-block::

        curl code


Then save the result (eg. ``URI:LIT:jbswy3dpeblw64tmmqfa`` )


Download the contents of the text file
--------------------------------------


.. code-block::

    $ tahoe --node-directory=tahoe-server/client0 get URI:LIT:jbswy3dpeblw64tmmqfa``.



Upload an image file
--------------------

.. code-block::

    $ tahoe --node-directory=tahoe-server/client0 put tahoe-logo.png
    200 OK
    URI:CHK:l3ve7ethyaweijd7tc5gq6hiyi:cx24itrljpfobcg2qb6ckk3c464lqkl3qi6gmtagwhs2zxxzaywq:1:1:2716

Download into a local file
--------------------------

Image files don't look good in the terminal, so you will write the contents to a file ::

    $ tahoe --node-directory=tahoe-server/client0 get URI:CHK:l3ve7ethyaweijd7tc5gq6hiyi:cx24itrljpfobcg2qb6ckk3c464lqkl3qi6gmtagwhs2zxxzaywq:1:1:2716 > logo-result.png


Use a viewer to see the image contents of the file.

First: smallest possible session save and retrieve some data
============================================================

    * (CLI only for now)
    * Send a string  to Tahoe
    * receive a fURL
    * retrieve string using the fURL
    * print the fURL
    * print the string

Example:

.. code-block::

    http://127.0.0.1:3456/uri/URI:DIR2:u63su5g3ejfylhezb5l6w763xq:p3goyai4uk6azmzwes5twm4o2rqn6d4mq7jn3br7g45jsonmwtha/


Web API using python
====================

Use the sample python code to interact with the Web API.::

    $ python -m private_facts.hello-world
    ...
    fURL=
    string = "Hello World"


Storing the fURL: treat fURLs as secret
=======================================

.. warning:: The risk of exposing sensitive data increases from here.

The previous examples do not store the fURL beyond running application. When the examples terminate, the fURL is gone.
Tahoe-lafs would not be useful unless we could reuse the fURLs.
From this point on we have to consider how we will protect the fURLs

Store the fURL to persist within the SAME session
=================================================

In this section, you will:
    * read an external filename(s) (passed as argument)
    * Store a { file }
    * receive a fURL
    * save the fURL in a local memory (eg. dict)
    * retrieve { file } using the fURL

.. note:: This example overlooks the security concern. Do not do this in production code.

Now we will insert several files into Tahoe and receive fURLs for each one.

The behavior of the insert script looks like:

.. code-block::

    $ python -m private_facts.insert {filename0, filename1, ...}
    ...
    fURL 0 = {hazardous_fURL}
    file0 = {filename0}
    ---
    fURL 1 = {hazardous_fURL}
    file1 = {filename1}


Store the URL with your code to persist across sessions
=======================================================

    * Store a { file, string }
    * receive a fURL
    * - save the fURL in a external persistence (eg. key: value, json.dump, etc) using a local reference.
    * - use the local reference to access the persistence
    * - retrieve the fURL from persistence
    * - retrieve the {file, string} from Tahoe using the fURL.

.. warning:: You are straddling the tahoe security perimeter. In production the app should protect the capability string.


Advanced persistence mechanisms
------------------------------

Options for production use (eg. "repository pattern"):
*   High exposure / less secure: sqlite https://sqlite-utils.datasette.io/en/stable/python-api.html
*   Low exposure / more secure: https://github.com/bitwarden/sdk-sm/tree/main/languages/python#readme

.. code-block::

    $ python -m private_facts.upload {filename0, filename1, ...}
    ...
    original_fURL = {hazardous_fURL}
    safe_URL= {sanitized_alias_of_fURL}
    file0 = {filename0}
    ---
    safe_URL = {hazardous_fURL}
    file1 = {filename1}

    $ python -m private_facts.retrieve {local_ref, local_ref, ...}

