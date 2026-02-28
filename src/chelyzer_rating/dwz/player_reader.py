from typing import cast
from urllib.request import urlopen

from chelyzer_rating.dwz.player import Player
from chelyzer_rating.dwz.tournament import Tournament


class PlayerReader:
    """CSV Reader for historical player data."""

    URL_TEMPLATE: str = "https://www.schachbund.de/php/dewis/spieler.php?pkz={player_id}&format=csv"
    HEADERS_PLAYER: tuple[str, ...] = (
        "id",
        "nachname",
        "vorname",
        "titel",
        "dwz",
        "dwzindex",
        "fideid",
        "fideelo",
        "fidetitel",
        "fidenation",
    )
    HEADERS_TOURNAMENT: tuple[str, ...] = (
        "turniercode",
        "turniername",
        "dwzalt",
        "dwzaltindex",
        "punkte",
        "partien",
        "nichtgewertet",
        "erwartungswert",
        "gegner",
        "koeffizient",
        "dwzneu",
        "dwzneuindex",
        "leistung",
    )

    @staticmethod
    def _get_dict_from_csv_row(headers: tuple[str, ...], row: str) -> dict[str, str]:
        row_items = row.split("|")
        return dict(zip(headers, row_items, strict=True))

    @classmethod
    def _fetch_player_csv(cls, player_id: int) -> list[str]:
        with urlopen(cls.URL_TEMPLATE.format(player_id=player_id)) as response:
            return cast("list[str]", response.read().decode("utf-8").splitlines())

    @classmethod
    def get_player_data(cls, player_id: int) -> tuple[Player, list[Tournament]]:
        """Return general data as well as tournament data for the given player."""
        headers_player_string = "|".join(cls.HEADERS_PLAYER)
        headers_tournament_string = "|".join(cls.HEADERS_TOURNAMENT)
        csv_lines = cls._fetch_player_csv(player_id)

        player_row_index = csv_lines.index(headers_player_string) + 1
        player_row_dict = cls._get_dict_from_csv_row(cls.HEADERS_PLAYER, csv_lines[player_row_index])
        player = Player(**player_row_dict)

        if headers_tournament_string not in csv_lines:
            return player, []
        tournament_row_start_index = csv_lines.index(headers_tournament_string) + 1

        tournament_row_dicts = [
            cls._get_dict_from_csv_row(cls.HEADERS_TOURNAMENT, row) for row in csv_lines[tournament_row_start_index:]
        ]

        tournaments = [Tournament(**row_dict) for row_dict in tournament_row_dicts]

        return player, tournaments
