from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

from platformdirs import user_data_dir
from sqlmodel import Session, SQLModel, create_engine

if TYPE_CHECKING:
    from sqlalchemy import Engine


class DatabaseManager:
    """Manager for the database."""

    PACKAGE_DIRECTORY = Path(user_data_dir(__package__, appauthor=False))
    DATABASE_PATH = PACKAGE_DIRECTORY / "database.db"

    def __init__(self) -> None:
        """Initialize the manager."""
        self.PACKAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.engine: Engine = create_engine(f"sqlite:///{self.DATABASE_PATH}")

    def create_tables(self) -> None:
        """Create all tables."""
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session]:
        """Return a session."""
        with Session(self.engine) as session:
            yield session


database_manager = DatabaseManager()
