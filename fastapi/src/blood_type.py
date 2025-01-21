"""Blood types."""

from enum import StrEnum

BloodType = StrEnum("BloodType",
                    ("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"))
