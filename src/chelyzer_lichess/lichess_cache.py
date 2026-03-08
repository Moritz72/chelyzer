from pathlib import Path

from platformdirs import user_data_dir
from pydantic import TypeAdapter

from chelyzer_lichess.models import Game, Study


class LichessCache:
    """Cache for lichess data."""

    PACKAGE_DIRECTORY = Path(user_data_dir(__package__, appauthor=False))
    STUDY_GAMES_DIRECTORY = PACKAGE_DIRECTORY / "study_games"

    def __init__(self) -> None:
        """Initialize the cache."""
        self.STUDY_GAMES_DIRECTORY.mkdir(parents=True, exist_ok=True)

    def get_study_games(self, study: Study) -> list[Game] | None:
        """Retrieve all games in the given study from cache."""
        path = self.STUDY_GAMES_DIRECTORY / f"{study.id}.json"

        if not path.exists():
            return None
        return TypeAdapter(list[Game]).validate_json(path.read_bytes())

    def set_study_games(self, study: Study, games: list[Game]) -> None:
        """Write all given games in the given study to cache."""
        path = self.STUDY_GAMES_DIRECTORY / f"{study.id}.json"
        path.write_bytes(TypeAdapter(list[Game]).dump_json(games))
