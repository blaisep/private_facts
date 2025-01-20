"""Testing tests."""

from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_simple() -> None:
    """Start with no users, then create one, fetch it, delete, should be gone."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    response = client.post("/fred?birthdate=1969-07-20",
                           json={
                               "blood_type": "ab+",
                               "zodiac_sign": "scorpio",
                               "meyers_briggs": {
                                   "ei": "i",
                                   "sn": "n",
                                   "tf": "t",
                                   "jp": "j"}})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "username": "fred",
        "birthdate": "1969-07-20",
        "dubious_characteristics": {
            "blood_type": "ab+",
            "zodiac_sign": "scorpio",
            "meyers_briggs": {
                "ei": "i",
                "sn": "n",
                "tf": "t",
                "jp": "j"}}}
    # Dup should fail
    response = client.post("/fred?birthdate=2000-01-01",
                           json={
                               "blood_type": "o-",
                               "zodiac_sign": "virgo",
                               "meyers_briggs": {
                                   "ei": "e",
                                   "sn": "s",
                                   "tf": "f",
                                   "jp": "p"}})
    assert response.status_code == status.HTTP_409_CONFLICT
    # One item should exist
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    # Delete it
    response = client.delete("/fred")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Actually deleted
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    # Delete again should fail
    response = client.delete("/fred")
    assert response.status_code == status.HTTP_404_NOT_FOUND
