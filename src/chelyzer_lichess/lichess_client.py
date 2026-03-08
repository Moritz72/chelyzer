import re
from urllib.request import Request, urlopen

from chelyzer_lichess.lichess_cache import LichessCache
from chelyzer_lichess.models import Game, Study


class LichessClient:
    """Client for sending requests to lichess."""

    BASE_URL = "https://lichess.org"
    STUDIES_PATH_TEMPLATE = "/api/study/by/{username}"
    STUDY_PATH_TEMPLATE = "/api/study/{study_id}.pgn"

    def __init__(self, token: str, *, use_cache: bool = True) -> None:
        """Initialize the client."""
        self.token: str = token
        self.use_cache: bool = use_cache
        self.cache: LichessCache = LichessCache()

    def get_user_studies(self, username: str) -> list[Study]:
        """Return all studies of the given user."""
        url = self.BASE_URL + self.STUDIES_PATH_TEMPLATE.format(username=username)
        request = Request(url, headers={"Authorization": f"Bearer {self.token}"})

        with urlopen(request) as response:
            study_text = response.read().decode("utf-8").strip()

        studies = [Study.model_validate_json(line) for line in study_text.splitlines()]
        return [study for study in studies if not study.is_ignored()]

    def get_study_games(self, study: Study) -> list[Game]:
        """Return all games within the given study."""
        if self.use_cache:
            games = self.cache.get_study_games(study)
            if games is not None:
                return games

        url = self.BASE_URL + self.STUDY_PATH_TEMPLATE.format(study_id=study.id)
        request = Request(url, headers={"Authorization": f"Bearer {self.token}"})

        with urlopen(request) as response:
            study_text = response.read().decode("utf-8").strip()

        games_texts = re.split(r"\n(?=\[Event )", study_text)
        games = [Game.from_pgn_text(pgn_text) for pgn_text in games_texts]

        self.cache.set_study_games(study, games)
        return games
