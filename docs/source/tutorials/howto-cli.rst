Using the Sample App Tutorial
=============================

Learn to integrate Tahoe-LAFS with your app using the Web API, let's start by interacting with the service using the CLI.

Set up your local

Use the CLI to move some files in and out of Tahoe-LAFS

Upload a simple string
----------------------

Begin by uploading a string using either the CLI, a python script, or a ``curl`` command.

.. tab:: CLI

    .. code-block:: bash

        $ python3 private_facts/src/hello_world/hello_world.py

.. tab:: Python

    .. code-block:: python

        BASE_URL =
        http = urllib3.PoolManager()
        def upload_string():
            """
            Upload the contents of the test string via the Tahoe client and return fURL.
            """
            resp = http.request(
                "PUT",
                "http://127.0.0.1:3456/uri/",
                "name:Abigail, heart_rate:82, bp:110/75,flow_rate:0,temp:98.6"
            )
            furl = resp.data.decode("utf-8")
            print(furl)
            return furl


.. tab:: Curl

    .. code-block::

        curl ...

Then save the result (eg. ``URI:LIT:jbswy3dpeblw64tmmqfa`` ) this will serve to refer to the data later.

.. note:: For very small strings (less than 53 bytes), the client will avoid relying on external storage.


Upload a longer string
======================

Summary:
Here we upload a longer string and observe the structure of the link that returns.


Upload a simple text file
==========================

Summary:
Uploading a file involves the local file/path. The type of file does not matter. When the file is retrieved,
the contents can be written to the same file, another local file, or a helper app.

        $ echo "Hello World" > hello.txt
        $ tahoe --node-directory=tahoe-server/client0 put ./hello.txt

Note the result ``URI: ...`` because the client needs that to find the file.

Download the contents of the text file
--------------------------------------

Summary:
Download the CONTENTS of the file, view it directly and write the contents to a local file.

.. code-block::

    $ tahoe --node-directory=tahoe-server/client0 get URI:LIT:jbswy3dpeblw64tmmqfa .

(the trailing ``.``  refers to the destination. In this case it writes to the terminal

But, what if we need to save the contents for later? Then we write to a local file and specify the type


Save the contents into a local file
-----------------------------------

Summary:
We can redirect the contents of the file using a redirection:

.. code-block::

        $ tahoe --node-directory=tahoe-server/client0 get URI:LIT:jbswy3dpeblw64tmmqfa`` > hello_back.txt


Upload an image (binary) file
=============================

Summary:
Upload a file with a binary type. In this case, a logo.

.. code-block::

    $ tahoe --node-directory=tahoe-server/client0 put tahoe-logo.png
    200 OK
    URI:CHK:l3ve7ethyaweijd7tc5gq6hiyi:cx24itrljpfobcg2qb6ckk3c464lqkl3qi6gmtagwhs2zxxzaywq:1:1:2716

Download into a local file
--------------------------

Image files don't look good in the terminal, so you will write the contents to a file ::

    $ tahoe --node-directory=tahoe-server/client0 get URI:CHK:l3ve7ethyaweijd7tc5gq6hiyi:cx24itrljpfobcg2qb6ckk3c464lqkl3qi6gmtagwhs2zxxzaywq:1:1:2716 > logo-result.png


Use a viewer to see the image contents of the file.

Web API using python
====================

Use the sample python code to interact with the Web API.::

    $ python -m private_facts.hello-world
    ...
    fURL=
    string = "name:Abigail, heart_rate:82, bp:110/75,flow_rate:0,temp:98.6"


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
-------------------------------

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

