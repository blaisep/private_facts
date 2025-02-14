from pydantic import BaseModel, Field, PlainValidator
from datetime import datetime
from typing import Annotated, Any


class PrivateFacts(BaseModel):
    """User facts of a sensitive and personal nature."""

    timestamp: "Timestamp"
    name: "User"
    pulse: "Pulse"
    bp: "Pressure"
    flow:  "Flow"
    temp: "Temperature"


def validate_pressure(value: Any) -> Any:
    if not isinstance(value, tuple):
        raise TypeError("Blood pressure must be a tuple.")
    systolic, diastolic = value
    if 50 <= diastolic <= 200 and 50 <= systolic <= 200:
        return value
    else:
        raise ValueError("That's not a valid blood pressure")


User = Annotated[str, Field(frozen=True, description="The user's first name.")]
Timestamp = Annotated[datetime, Field(frozen=True)]
Pulse = Annotated[int, Field(ge=30, le=250, frozen=True)]
Pressure = Annotated[
    tuple[int, int],
    Field(
        description="Blood pressure in mmHg (systolic, diastolic).",
        validator=PlainValidator(validate_pressure),
        frozen=True
    )
]
Flow = Annotated[int, Field(ge=30, le=250, frozen=True), "Number of product used in 24 hour period."]
Temperature = Annotated[float, Field(ge=50, le=250, frozen=True), "Body temperature in degrees Fahrenheit."]
