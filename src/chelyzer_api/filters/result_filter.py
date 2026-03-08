from chelyzer_api.enums import GameResult
from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class ResultFilter(BaseFilter):
    """Game filter for result."""

    def __init__(self, results: list[GameResult]) -> None:
        """Initialize the filter."""
        self._results: set[GameResult] = set(results)

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for their result."""
        return [game for game in games if GameResult.from_game(game) in self._results]
