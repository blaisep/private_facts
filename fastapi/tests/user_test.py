"""Testing tests."""

from fastapi import status
from fastapi.testclient import TestClient
import pytest

from src.main import app

client = TestClient(app)

@pytest.fixture()
def basic_user():
    pass


def test_root_path() -> None:
    """The app returns a valid path ."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_create_user() -> None:
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

    get_created_user = client.get("/")
    assert get_created_user.status_code == status.HTTP_200_OK
    assert len(get_created_user.json()) == 1


def test_create_duplicate_username_fails() -> None:
    first_user = client.post("/fred?birthdate=1969-07-20",
                           json={
                               "blood_type": "ab+",
                               "zodiac_sign": "scorpio",
                               "meyers_briggs": {
                                   "ei": "i",
                                   "sn": "n",
                                   "tf": "t",
                                   "jp": "j"}})
    second_user = client.post("/fred?birthdate=2000-01-01",
                           json={
                               "blood_type": "o-",
                               "zodiac_sign": "virgo",
                               "meyers_briggs": {
                                   "ei": "e",
                                   "sn": "s",
                                   "tf": "f",
                                   "jp": "p"}})

    assert second_user.status_code == status.HTTP_409_CONFLICT

def test_delete_user():
    user = client.post("/fred?birthdate=1969-07-20",
                           json={
                               "blood_type": "ab+",
                               "zodiac_sign": "scorpio",
                               "meyers_briggs": {
                                   "ei": "i",
                                   "sn": "n",
                                   "tf": "t",
                                   "jp": "j"}})

    response = client.delete("/fred")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Actually deleted
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    response = client.delete("/fred")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_read_user() -> None:
    pass