import os
from typing import TYPE_CHECKING

from chelyzer_lichess import LichessClient

if TYPE_CHECKING:
    from chelyzer_lichess.models import Game


def test_get_study() -> None:
    """Test retrieval of studies."""
    study_id = "QS1Qv4Wd"

    username = os.getenv("LICHESS_USERNAME", "")
    token = os.getenv("LICHESS_API_TOKEN", "")
    client = LichessClient(token)

    studies = client.get_user_studies(username)
    games: list[Game] | None = None

    for study in studies:
        if study.id == study_id:
            games = client.get_study_games(study)

    assert games is not None
