"""
Conftest tests
"""
from abc import ABC, abstractmethod

"""
Fake node

Repository Pattern? Object that responds to requests for read, write, metadata, delete...
"""
# class AbstractNode(abc.ABC):
#     @abc.abstractmethod


    """ Storage class
    """

    """
    Introducer Class
    """

"""
Domain Model: the problem we're trying to solve:

begin with content, replace it with a token, 
map that token to a number of (encrypted) fragments
permute the token to accommodate different conditions (privileges, constraints, etc.)
use the token to retrieve the fragments.
reconstruct the content from the fragments.

The solution looks like this:
- some Content (clear) sent to a process
- service-layer (tahoe-client) converts content to fragments (cipher)
- service-layer assigns a token to the collection of fragments
- service-layer associates capabilities to the token
- finally, the service-layer sends fragments to repository (tahoe-server)
- repository disperses fragments to storage (persistence)

"""