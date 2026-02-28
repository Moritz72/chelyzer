from pydantic import BaseModel


class Player(BaseModel):
    """Model for player data."""

    id: str
    nachname: str
    vorname: str
    titel: str
    dwz: str
    dwzindex: str
    fideid: str
    fideelo: str
    fidetitel: str
    fidenation: str
