from abc import ABC, abstractmethod
from datetime import date


class BaseRatingClient(ABC):
    """Abstract client for retrieving rating information."""

    @abstractmethod
    def get_id(self, player_name: str) -> int:
        """Return the ID of the player with the given name."""

    @abstractmethod
    def get_name(self, player_id: int) -> str:
        """Return the name of the player with the given ID."""

    @abstractmethod
    def get_rating_by_id(self, player_id: int, rating_date: date) -> int | None:
        """Return the rating of the player with the given ID at the given date."""

    def get_rating_by_name(self, player_name: str, rating_date: date) -> int | None:
        """Return the rating of the player with the given name at the given date."""
        player_id = self.get_id(player_name)
        return self.get_rating_by_id(player_id, rating_date)
