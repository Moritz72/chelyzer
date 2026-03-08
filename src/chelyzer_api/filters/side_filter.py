from chelyzer_api.enums import GameSide
from chelyzer_api.filters.base_filter import BaseFilter
from chelyzer_lichess.models import FullyAnnotatedGame


class SideFilter(BaseFilter):
    """Game filter for side."""

    def __init__(self, player_name: str, sides: list[GameSide]) -> None:
        """Initialize the filter."""
        self._player_name: str = player_name
        self._sides: set[GameSide] = set(sides)

    def _is_side_match(self, game: FullyAnnotatedGame, side: GameSide) -> bool:
        """Check whether the player has the correct side in the given game."""
        if side == GameSide.WHITE:
            return game.white == self._player_name
        return game.black == self._player_name

    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Filter the given list of games for the player's side."""
        if len(self._sides) == 0:
            return []
        if len(self._sides) > 1:
            return games
        return [game for game in games if self._is_side_match(game, next(iter(self._sides)))]
