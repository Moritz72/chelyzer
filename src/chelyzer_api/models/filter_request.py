from datetime import date

from pydantic import BaseModel

from chelyzer_api.enums import GameResult, GameSide, Opening


class FilterRequest(BaseModel):
    """Model for a filter request."""

    sides: list[GameSide] | None = None
    results: list[GameResult] | None = None
    min_rating: int | None = None
    max_rating: int | None = None
    min_plies: int | None = None
    max_plies: int | None = None
    min_date: date | None = None
    max_date: date | None = None
    openings: list[Opening] | None = None
