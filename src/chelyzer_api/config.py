import os

from dotenv import load_dotenv

from chelyzer_lichess import LichessClient
from chelyzer_rating import BaseRatingClient, DwzClient

load_dotenv()

_rating_clients = {"DWZ": DwzClient}


def _get_environment_variable(name: str) -> str:
    """Return the environment variable with the given name and raise an error if it is not set."""
    variable = os.getenv(name)

    if variable is None:
        error_message = f"'{name}' environment variable is not set"
        raise ValueError(error_message)

    return variable


def _get_rating_client(client_name: str) -> BaseRatingClient:
    client = _rating_clients.get(client_name)

    if client is None:
        error_message = f"Unknown rating client '{client_name}'"
        raise ValueError(error_message)

    return client()


class Config:
    """Configuration read from the environment."""

    lichess_client: LichessClient = LichessClient(_get_environment_variable("LICHESS_API_TOKEN"))
    lichess_username: str = _get_environment_variable("LICHESS_USERNAME")
    rating_client: BaseRatingClient = _get_rating_client(_get_environment_variable("RATING_CLIENT"))
    player_name: str = _get_environment_variable("PLAYER_NAME")
