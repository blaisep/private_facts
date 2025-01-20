"""
Tests for the storage module.
"""
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

"""
Connect to Tahoe.
"""
def test_get_simple():
    uri = ""
    filecap = ""
    url = f"/{uri}/{filecap}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK



"""
Check access to tahoe secure storage service.
"""

"""
Create directory cap named YYYY-MM-DD.
"""

"""
READ directory cap named YYYY-MM-DD.
"""

"""
Write the file cap to secure local storage service.

"""

"""
READ the most recent file
"""

"""
DELETE the most recent file
"""

# --- If we pull content from Tahoe to store locally...

"""
Check access to local secure storage service.
"""