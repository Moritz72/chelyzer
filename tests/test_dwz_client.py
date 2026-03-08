import os
from datetime import date

import pytest

from chelyzer_rating import DwzClient
from chelyzer_rating.dwz.models import DsbCredentials


@pytest.mark.skipif(os.getenv("CI") == "true", reason="Skip on CI")
def test_get_rating() -> None:
    """Test retrieval of ratings at various dates."""
    username = os.getenv("DSB_USERNAME", "")
    password = os.getenv("DSB_PASSWORD", "")

    credentials = DsbCredentials(username=username, password=password)
    client = DwzClient(credentials=credentials)

    player_name = "Eckert, Moritz"
    year_to_rating = {
        2017: None,
        2018: None,
        2019: 1433,
        2020: 1737,
        2021: 1730,
        2022: 1730,
        2023: 1808,
        2024: 1856,
        2025: 1896,
    }

    for year, rating in year_to_rating.items():
        rating_date = date(year, 1, 1)
        client_rating = client.get_rating_by_name(player_name, rating_date)
        assert client_rating == rating
