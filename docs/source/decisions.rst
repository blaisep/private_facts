====================
Decision Records
====================


TDD: When to write tests?
==========================

(Starting with a blank page?)


SQLite?
=======

Read/write to to SQLite on start/exit (and write to local file for cache)
(otherwise mod SQLite to use Tahoe)
write to redis on the fly (for caching) : more dependencies

Time Zone for date field?
=========================

UTC would be best and then (optionally display in the user's locale?)

Kelvin for temp
===============

Should I collect from user in C or F rather than force them to enter Kelvin?

Flow rate from 0 - 50
=====================

Should the upper boundary be lower?


Choose an HTTP client for the examples
======================================

requests

SQLite for the "database" in Private facts


Introduce the file/path metaphor later?
=======================================

Do it later

Other pending content
=====================

Footnote on the LIT (for short items, that don't even leave the client)

Domain Model
============

https://www.cosmicpython.com/book/chapter_01_domain_model.html#_what_is_a_domain_model

Entity
Value Object
Domain Service


Entity
------

    * User Account

Value Object
------------

    * fURL
    * Content
    * Metadata (alias, path, directory)


A user uploads content, they send a file and get a fURL

app -> a

User downloads content, they send a fURL and get the content

User creates a directory, they send a name (path?) and get fURL

(User does not update)

User deletes a file, they send a fURL and a delete

Control Plane
=============

Tahoe commands over Foolscap ("the API")

Data Plane
==========

Content over HTTPS

