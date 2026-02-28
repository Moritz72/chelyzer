from datetime import date

from chelyzer_rating import DwzClient


def test_get_rating() -> None:
    """Test retrieval of rating at various dates."""
    client = DwzClient()
    player_name = "Moritz Eckert"
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
