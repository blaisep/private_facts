==============
Private Facts
==============




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

