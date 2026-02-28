from pathlib import Path

from platformdirs import user_data_dir

CACHE_DIRECTORY = Path(user_data_dir(__package__, appauthor=False))
CACHE_DIRECTORY.mkdir(parents=True, exist_ok=True)
