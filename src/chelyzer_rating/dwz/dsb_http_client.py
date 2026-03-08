import base64
import csv
import io
import re
import zipfile
from datetime import date, datetime

import requests

from chelyzer_rating.dwz.models import DsbCredentials, Player


class DsbHttpClient:
    """Client for sending requests to the Deutscher Schachbund website."""

    BASE_URL = "https://www.schachbund.de"
    BROKEN_DATES = frozenset({date(2022, 5, 22), date(2024, 1, 30)})

    def __init__(self, credentials: DsbCredentials) -> None:
        """Initialize the client."""
        self.session: requests.Session = requests.Session()

        self._login(credentials)

    def _login(self, credentials: DsbCredentials) -> None:
        """Login to the Deutscher Schachbund website."""
        url = f"{self.BASE_URL}/anmelden.html"

        payload = {
            "FORM_SUBMIT": "tl_login_180",
            "_target_path": base64.b64encode(url.encode()).decode(),
            "username": credentials.username,
            "password": credentials.password,
        }

        response = self.session.post(url, data=payload)
        response.raise_for_status()

    def get_list_dates(self) -> list[date]:
        """Get the list of dates for which there is a DWZ list available."""
        url = f"{self.BASE_URL}/dwz-archiv-downloads-dsb.html"

        response = self.session.get(url)
        response.raise_for_status()

        pattern = r'"dwz-archiv-downloads-dsb\.html\?file=files/dewis/\d{4}/csv/LV-0-csv_(\d{8})\.zip"'
        date_strings = re.findall(pattern, response.text)

        return sorted({datetime.strptime(date_string, "%Y%m%d").date() for date_string in date_strings})

    def get_player_list(self, list_date: date) -> set[Player]:
        """Get the players in the DWZ list of the given date."""
        if list_date in self.BROKEN_DATES:
            return set()

        date_string = list_date.strftime("%Y%m%d")
        year_string = list_date.strftime("%Y")

        url = f"{self.BASE_URL}/dwz-archiv-downloads-dsb.html"
        params = f"file=files/dewis/{year_string}/csv/LV-0-csv_{date_string}.zip"
        url = f"{url}?{params}"

        response = self.session.get(url)
        response.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(response.content)) as zf, zf.open("spieler.csv") as f:
            content = f.read().decode("cp1252")

        reader = csv.DictReader(io.StringIO(content), delimiter=",")
        rows = (row for row in reader if row["Geburtsjahr"] != "")
        return {Player.model_validate(row) for row in rows}
