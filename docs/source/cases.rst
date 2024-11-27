====
FAQ
====

What does Tahoe (not) do for you?
=================================

Tahoe doesn't make storing secrets go away, it just makes them smaller.
The capabilities are NOT dependent on the provider.

Basic Scenarios
===============

A file is stored in cipher on the cloud *HOWEVER* the cap is in the clear
* Availability
    * Access Control (verify)
    * Access Control (sharing)
    * Access Control (write)
* encryption at rest
RISK: the cap is in the clear

Incomplete
----------

A file is store in cipher on the cloud *AND* the cap is secret
* Availability
    * Access Control (verify)
    * Access Control (sharing)
    * Access Control (write)
* encryption at rest
* Confidentiality (cap is secured) **UNLESS** clear in the client

Complete
--------

A doc is store in cipher on the cloud *and* user app (using a local binary)
"end to encryptions"
* Availability
    * Access Control (verify)
    * Access Control (sharing)
    * Access Control (write)
* encryption at rest
* Confidentiality (cap is secured)

Delete
    The reference(s) to the shares is removed. The shares may still exist, but there is no way to find them.

Recover
    regain access to content on an existing device

Restore
    copy data onto a new device (eg. the reverse of backup)

Threat Surfaces
===============

Front end
    The part facing the human is the front end. Front end is outside of the Tahoe-lafs security domain. Content is in the clear, unless the front end limits exposure somehow.

Client
    The client moves content in and out of Tahoe-lafs. A client creates the capability string and (de)crypts the content in the shares. The tahoe-lafs security boundary is in the client.

Storage node
    Storage nodes contain "shares" (fragments) in cipher.

Grid
    Storage nodes can be accessed from one or more introducers. The collection of nodes an introducer can access is called a grid.

Introducer
    An introducer may be shared or private, depending on how much exposure a user can tolerate. Each introducer has the map of fURL to storages nodes, but the Client decrypts the shares from the storage nodes.

Authentication
    A shared introducer might use a method of granting access to a request from a client. (??)

Use Cases
=========

User collects data from disparate sources for long term storage. (eg. medical records from all providers. User doesn't know when they will need the records but they don't want to risk losing them. A community grid will self replicate indefinitely.