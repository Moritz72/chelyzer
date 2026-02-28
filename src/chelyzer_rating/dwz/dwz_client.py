from datetime import date

from chelyzer_rating.base import BaseRatingClient
from chelyzer_rating.dwz.player_cache import PlayerCache
from chelyzer_rating.dwz.player_reader import PlayerReader


class DwzClient(BaseRatingClient):
    """Rating client for DWZ."""

    def __init__(self) -> None:
        """Initialize a new client."""
        self._player_cache: PlayerCache = PlayerCache()

    def get_id(self, player_name: str) -> int:
        """Return the ID of the player with the given name."""
        return self._player_cache.get_id(player_name)

    def get_name(self, player_id: int) -> str:
        """Return the name of the player with the given ID."""
        return self._player_cache.get_name(player_id)

    def get_rating_by_id(self, player_id: int, rating_date: date) -> int | None:
        """Return the rating of the player with the given ID at the given date."""
        _, tournaments = PlayerReader.get_player_data(player_id)

        most_recent = next(
            (tournament for tournament in reversed(tournaments) if tournament.end_date <= rating_date), None
        )

        if most_recent is None:
            return None
        dwz_string = most_recent.dwzneu

        if dwz_string:
            return int(dwz_string)
        return None
