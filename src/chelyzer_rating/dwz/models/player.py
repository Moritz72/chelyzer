from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


def _empty_str_to_none(string: str) -> str | None:
    if string == "":
        return None
    return string


class Player(BaseModel):
    """Model for player data."""

    name: str = Field(..., alias="Spielername")
    birthyear: int = Field(..., alias="Geburtsjahr")
    dwz: Annotated[int | None, BeforeValidator(_empty_str_to_none)] | None = Field(..., alias="DWZ")

    def __eq__(self, other: object) -> bool:
        """Return true if both objects are equal."""
        if not isinstance(other, Player):
            return NotImplemented
        return self.name == other.name and self.birthyear == other.birthyear

    def __hash__(self) -> int:
        """Return hash of the object."""
        return hash((self.name, self.birthyear))
