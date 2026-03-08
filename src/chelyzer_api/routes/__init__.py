from chelyzer_api.routes.games import games_router
from chelyzer_api.routes.options import options_router

routers = [games_router, options_router]

__all__ = ["routers"]
