import csv
import io
import json
import urllib.request
import zipfile
from typing import cast

from chelyzer_rating.cache import CACHE_DIRECTORY


class PlayerCache:
    """Cache for player name and ID lookup."""

    DOWNLOAD_URL = "https://dwz.svw.info/services/files/export/csv/LV-0-csv_v2.zip"
    CACHE_FILE_PATH = CACHE_DIRECTORY / "dwz_client_player_cache.json"

    def __init__(self, refresh: bool = False) -> None:
        """Initialize a new cache instance."""
        if refresh or not self.CACHE_FILE_PATH.exists():
            self._write_data()

        self._name_to_id: dict[str, int] = self._read_data()
        self._id_to_name: dict[int, str] = {
            player_id: player_name for player_name, player_id in self._name_to_id.items()
        }

    def _read_data(self) -> dict[str, int]:
        return cast("dict[str, int]", json.loads(self.CACHE_FILE_PATH.read_text(encoding="utf-8")))

    def _write_data(self) -> None:
        with urllib.request.urlopen(self.DOWNLOAD_URL) as response:
            zip_data = response.read()

        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf, zf.open("spieler.csv") as f:
            content = f.read().decode("cp1252")

        reader = csv.DictReader(io.StringIO(content), delimiter=",")
        name_to_id = {" ".join(reversed(row["Spielername"].split(","))): int(row["ID"]) for row in reader}

        self.CACHE_FILE_PATH.write_text(json.dumps(name_to_id, indent=4), encoding="utf-8")

    def get_id(self, player_name: str) -> int:
        """Retrieve the ID for the given name."""
        return self._name_to_id[player_name]

    def get_name(self, player_id: int) -> str:
        """Retrieve the name for the given ID."""
        return self._id_to_name[player_id]
