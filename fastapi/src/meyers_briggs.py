"""Meyers Briggs personality types."""

from enum import StrEnum
from pydantic import BaseModel

EI = StrEnum("EI", ("E", "I"))
SN = StrEnum("SN", ("S", "N"))
TF = StrEnum("TF", ("t", "f"))
JP = StrEnum("JP", ("j", "p"))

class MeyersBriggs(BaseModel):
    """Define Meyers Briggs personality types.

    https://www.myersbriggs.org/my-mbti-personality-type/myers-briggs-overview/
    """

    ei: EI
    sn: SN
    tf: TF
    jp: JP
