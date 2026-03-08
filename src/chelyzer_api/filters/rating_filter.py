from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class RatingFilter(BaseFilter):
    """Game filter for rating."""

    def __init__(self, player_name: str, min_rating: int | None = None, max_rating: int | None = None) -> None:
        """Initialize the filter."""
        self._player_name: str = player_name
        self._min_rating: int = min_rating or 0
        self._max_rating: int = max_rating or 9999

    def _get_relative_rating(self, game: FullyAnnotatedGame) -> int:
        """Return the rating of the opponent in the given game."""
        if game.white == self._player_name:
            return game.black_rating or 0
        return game.white_rating or 0

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for their opponent ratings."""
        return [game for game in games if self._min_rating <= self._get_relative_rating(game) < self._max_rating]
