from enum import StrEnum

from chelyzer_lichess.models import FullyAnnotatedGame


class GameResult(StrEnum):
    """Enum for the result of a game."""

    WIN = "1:0"
    DRAW = "½:½"
    LOSS = "0:1"
    FORFEIT_WIN = "+:-"
    FORFEIT_LOSS = "-:+"

    @classmethod
    def from_game(cls, game: FullyAnnotatedGame) -> GameResult:  # noqa: F821
        """Return a game result instance from the given game."""
        if game.termination == "forfeit":
            match game.result:
                case "1-0":
                    return GameResult.FORFEIT_WIN
                case "0-1":
                    return GameResult.FORFEIT_LOSS
                case _:
                    error_message = f"Undefined forfeit result '{game.result}'"
                    raise ValueError(error_message)

        match game.result:
            case "1-0":
                return GameResult.WIN
            case "1/2-1/2":
                return GameResult.DRAW
            case "0-1":
                return GameResult.LOSS
            case _:
                error_message = f"Undefined result '{game.result}'"
                raise ValueError(error_message)

    def get_flipped(self) -> GameResult:  # noqa: F821
        """Return the reverse result to the given instance."""
        match self:
            case GameResult.WIN:
                return GameResult.LOSS
            case GameResult.LOSS:
                return GameResult.WIN
            case GameResult.FORFEIT_WIN:
                return GameResult.FORFEIT_LOSS
            case GameResult.FORFEIT_LOSS:
                return GameResult.FORFEIT_WIN
            case _:
                return GameResult.DRAW
