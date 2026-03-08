from chelyzer_api.enums import Opening
from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class OpeningFilter(BaseFilter):
    """Game filter for opening."""

    def __init__(self, openings: list[Opening]) -> None:
        """Initialize the filter."""
        self._openings: set[Opening] = set(openings)

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for the opening."""
        return [game for game in games if Opening.from_game(game) in self._openings]
