from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class PlyFilter(BaseFilter):
    """Game filter for plies."""

    def __init__(self, min_plies: int | None = None, max_plies: int | None = None) -> None:
        """Initialize the filter."""
        self._min_plies: int = min_plies or 0
        self._max_plies: int = max_plies or 9999

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for their plies."""
        return [game for game in games if self._min_plies <= game.plies < self._max_plies]
