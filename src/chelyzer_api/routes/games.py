from fastapi import APIRouter

from chelyzer_api.config import Config
from chelyzer_api.filters import (
    BaseFilter,
    DateFilter,
    OpeningFilter,
    PlyFilter,
    RatingFilter,
    ResultFilter,
    SideFilter,
)
from chelyzer_api.game_store import GameStore
from chelyzer_api.models import FilterRequest
from chelyzer_lichess.models.game import FullyAnnotatedGame

games_router = APIRouter(prefix="/games", tags=["games"])
game_store = GameStore(Config.lichess_client, Config.rating_client, Config.lichess_username)


@games_router.post("/filtered", response_model=list[FullyAnnotatedGame])
def get_filtered_games(filter_request: FilterRequest) -> list[FullyAnnotatedGame]:
    """Return all games filtered by the given request."""
    games = game_store.games
    filters: list[BaseFilter] = []

    if filter_request.sides is not None:
        filters.append(SideFilter(Config.player_name, filter_request.sides))
    if filter_request.results is not None:
        filters.append(ResultFilter(filter_request.results))
    if filter_request.openings is not None:
        filters.append(OpeningFilter(filter_request.openings))
    filters.append(DateFilter(filter_request.min_date, filter_request.max_date))
    filters.append(PlyFilter(filter_request.min_plies, filter_request.max_plies))
    filters.append(RatingFilter(Config.player_name, filter_request.min_rating, filter_request.max_rating))

    for game_filter in filters:
        games = game_filter.apply(games)

    return games
