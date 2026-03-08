from chelyzer_lichess import LichessClient
from chelyzer_lichess.models import FullyAnnotatedGame, Game
from chelyzer_rating import BaseRatingClient


class GameStore:
    """Store for games."""

    def __init__(self, lichess_client: LichessClient, rating_client: BaseRatingClient | None, username: str) -> None:
        """Initialize the analyzer."""
        self.games: list[FullyAnnotatedGame] = self._get_games(lichess_client, rating_client, username)

    @staticmethod
    def _get_games(
        lichess_client: LichessClient, rating_client: BaseRatingClient | None, username: str
    ) -> list[FullyAnnotatedGame]:
        """Return a flat list of all games within the studies of the given user."""
        studies = lichess_client.get_user_studies(username)
        games = [game for study in studies for game in lichess_client.get_study_games(study)]

        annotated_games: list[FullyAnnotatedGame] = [game for game in games if Game.is_fully_annotated(game)]
        if len(annotated_games) != len(games):
            missing_games = [game.event or "Unknown" for game in games if game not in annotated_games]
            error_message = "The following games were not annotated: {}".format(", ".join(missing_games))
            raise Exception(error_message)

        if rating_client is None:
            return annotated_games

        for game in annotated_games:
            game.white_rating = rating_client.get_rating_by_name(game.white, game.date)
            game.black_rating = rating_client.get_rating_by_name(game.black, game.date)

        return annotated_games
