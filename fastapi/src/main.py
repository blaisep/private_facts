"""main program for FastAPI."""

from __future__ import annotations

from datetime import date
from fastapi import FastAPI, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from typing import Annotated

from .blood_type import BloodType
from .meyers_briggs import MeyersBriggs
from .zodiac_sign import ZodiacSign


app = FastAPI()
today = date.today()

class DubiousCharacteristics(BaseModel):
    """User characteristics of questionable value."""

    blood_type: BloodType
    zodiac_sign: ZodiacSign
    meyers_briggs: MeyersBriggs


Str1To64 = Annotated[str, Field(min_length=1,
                                max_length=64)]


class User(BaseModel):
    """Simple User."""

    username: Str1To64
    birthdate: date
    dubious_characteristics: DubiousCharacteristics


users: dict[str, User] = {}


@app.get("/",
         status_code=status.HTTP_200_OK,
         response_model=list[User])
async def list_users() -> list[User]:
    """List users stored in RAM."""

    return list(users.values())

birthdate_validation = Query(description="YEAR-MO-DT")

@app.post("/{username}",
          status_code=status.HTTP_201_CREATED,
          response_model=User)
async def add_user(username: Str1To64,
                   dubious_characteristics: DubiousCharacteristics,
                   birthdate: date = birthdate_validation) -> User:
    """Store user info in RAM."""

    if username in users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User {username} already exists")
    users[username] = User(username=username,
                           birthdate=birthdate,
                           dubious_characteristics=dubious_characteristics)

    return users[username]

@app.delete("/{username}")
async def delete_user(username: str) -> Response:
    """Remove user from RAM."""

    try:
        del users[username]
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e

    return Response(status_code=status.HTTP_204_NO_CONTENT)
