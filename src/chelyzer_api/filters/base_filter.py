from abc import ABC, abstractmethod

from chelyzer_lichess.models import FullyAnnotatedGame


class BaseFilter(ABC):
    """Base class for filtering games."""

    @abstractmethod
    def apply(self, games: list[FullyAnnotatedGame]) -> list[FullyAnnotatedGame]:
        """Apply the filter to the given list of games."""
