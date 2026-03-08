from datetime import date

from sqlmodel import desc, select

from chelyzer_rating.base import BaseRatingClient
from chelyzer_rating.database_manager import database_manager
from chelyzer_rating.dwz.dsb_http_client import DsbHttpClient
from chelyzer_rating.dwz.models import DsbCredentials, PlayerDwz
from chelyzer_rating.dwz.table_manager import TableManager


class DwzClient(BaseRatingClient):
    """Rating client for DWZ."""

    def __init__(self, *, credentials: DsbCredentials | None = None) -> None:
        """Initialize the client."""
        database_manager.create_tables()

        if credentials is None:
            return

        client = DsbHttpClient(credentials)
        table_manager = TableManager(client)

        with database_manager.get_session() as session:
            table_manager.update(session)

    def get_rating_by_name(self, player_name: str, list_date: date) -> int | None:
        """Return the rating of the player with the given name at the given date."""
        player_name = player_name.replace(", ", ",")

        with database_manager.get_session() as session:
            query = (
                select(PlayerDwz.dwz)
                .where(PlayerDwz.name == player_name)
                .where(PlayerDwz.list_date <= list_date)
                .order_by(desc(PlayerDwz.list_date))
                .limit(1)
            )

            dwz = session.exec(query).first()
            return dwz if dwz else None
