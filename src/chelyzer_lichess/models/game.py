import io
import re
from datetime import date, datetime
from typing import Self, TypeGuard

import chess.pgn
from pydantic import BaseModel


def _get_annotation_count(pgn_text: str, annotation: str) -> int:
    """Count the number of occurrences of a given annotation."""
    pattern = rf"\{{[^}}]*?{annotation}[^}}]*?\}}"
    matches = re.findall(pattern, pgn_text)

    return len(matches)


def _parse_int(value: str | None) -> int | None:
    """Safely parse an integer, returning None for missing values."""
    if value is None:
        return None
    return int(value)


def _parse_date(value: str | None) -> date | None:
    """Parse a PGN date string, returning None for missing values."""
    if value is None:
        return None
    return datetime.strptime(value, "%Y.%m.%d").date()


class Game(BaseModel):
    """Model for a lichess game."""

    white: str | None
    white_rating: int | None
    black: str | None
    black_rating: int | None
    result: str | None
    termination: str | None
    date: date | None
    event: str | None
    plies: int
    opening: str
    inaccuracies: int
    mistakes: int
    blunders: int

    @classmethod
    def from_pgn_text(cls, pgn_text: str) -> Self:
        """Return a game instance from a given PGN text."""
        game = chess.pgn.read_game(io.StringIO(pgn_text))

        if game is None:
            error_message = "Invalid PGN text"
            raise ValueError(error_message)

        headers = game.headers
        moves = [move.uci() for move in game.mainline_moves()]

        return cls(
            white=headers.get("White"),
            white_rating=_parse_int(headers.get("WhiteElo")),
            black=headers.get("Black"),
            black_rating=_parse_int(headers.get("BlackElo")),
            result=headers.get("Result"),
            termination=headers.get("Termination"),
            date=_parse_date(headers.get("Date")),
            event=headers.get("Event"),
            plies=len(moves),
            opening=headers.get("Opening", "?"),
            inaccuracies=_get_annotation_count(pgn_text, "Inaccuracy"),
            mistakes=_get_annotation_count(pgn_text, "Mistake"),
            blunders=_get_annotation_count(pgn_text, "Blunder"),
        )

    @staticmethod
    def is_fully_annotated(game: Game) -> TypeGuard[FullyAnnotatedGame]:  # noqa: F821
        """Check whether a given game is fully annotated."""
        return (
            game.white is not None
            and game.black is not None
            and game.result is not None
            and game.date is not None
            and game.event is not None
        )


class FullyAnnotatedGame(Game):
    """Model for a lichess game with all annotations present."""

    white: str
    white_rating: int | None
    black: str
    black_rating: int | None
    result: str
    date: date
    event: str
