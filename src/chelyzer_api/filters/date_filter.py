from datetime import date

from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class DateFilter(BaseFilter):
    """Game filter for date."""

    def __init__(self, min_date: date | None = None, max_date: date | None = None) -> None:
        """Initialize the filter."""
        self._min_date: date = min_date or date.min
        self._max_date: date = max_date or date.max

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for their date."""
        return [game for game in games if self._min_date < game.date < self._max_date]
