from datetime import date

from sqlmodel import Session, and_, col, desc, func, select

from chelyzer_rating.dwz.dsb_http_client import DsbHttpClient
from chelyzer_rating.dwz.models import PlayerDwz


class TableManager:
    """Manager for updating the player DWZ table."""

    def __init__(self, http_client: DsbHttpClient) -> None:
        """Initialize the table manager."""
        self.http_client: DsbHttpClient = http_client

    @staticmethod
    def _get_most_recent_date(session: Session) -> date:
        query = select(PlayerDwz).order_by(desc(PlayerDwz.list_date)).limit(1)
        player_dwz = session.exec(query).first()

        if player_dwz is None:
            return date.min
        return player_dwz.list_date

    def _add_entries(self, session: Session, list_date: date) -> None:
        players = self.http_client.get_player_list(list_date)

        latest_date_sub_query = (
            select(PlayerDwz.name, PlayerDwz.birthyear, func.max(PlayerDwz.list_date).label("max_date"))
            .group_by(col(PlayerDwz.name), col(PlayerDwz.birthyear))
            .subquery()
        )
        latest_dwz_query = select(PlayerDwz).join(
            latest_date_sub_query,
            and_(
                PlayerDwz.name == latest_date_sub_query.c.name,
                PlayerDwz.birthyear == latest_date_sub_query.c.birthyear,
                PlayerDwz.list_date == latest_date_sub_query.c.max_date,
            ),
        )

        latest_dwz_rows = session.exec(latest_dwz_query).all()
        current_dwz = {(row.name, row.birthyear): row.dwz for row in latest_dwz_rows}

        to_insert = [
            PlayerDwz(name=player.name, birthyear=player.birthyear, list_date=list_date, dwz=player.dwz)
            for player in players
            if player.dwz is not None and player.dwz != current_dwz.get((player.name, player.birthyear))
        ]

        session.add_all(to_insert)
        session.commit()

    def update(self, session: Session) -> None:
        """Add all updated entries of all new DWZ lists to the table."""
        list_dates = self.http_client.get_list_dates()
        most_recent_date = self._get_most_recent_date(session)
        dates_to_add = [list_date for list_date in list_dates if list_date > most_recent_date]

        for list_date in dates_to_add:
            self._add_entries(session, list_date)
