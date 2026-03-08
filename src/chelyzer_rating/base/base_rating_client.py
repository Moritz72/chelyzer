from abc import ABC, abstractmethod
from datetime import date


class BaseRatingClient(ABC):
    """Abstract client for retrieving rating information."""

    @abstractmethod
    def get_rating_by_name(self, player_name: str, rating_date: date) -> int | None:
        """Return the rating of the player with the given name at the given date."""
