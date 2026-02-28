from datetime import date

from pydantic import BaseModel


class Tournament(BaseModel):
    """Model for tournament data."""

    turniercode: str
    turniername: str
    dwzalt: str
    dwzaltindex: str
    punkte: str
    partien: str
    nichtgewertet: str
    erwartungswert: str
    gegner: str
    koeffizient: str
    dwzneu: str
    dwzneuindex: str
    leistung: str

    @property
    def end_date(self) -> date:
        """Return the estimated end date."""
        decade = ord(self.turniercode[0].upper()) - ord("A")
        unit = int(self.turniercode[1])

        year = 2000 + decade * 10 + unit
        week = int(self.turniercode[2:4])

        return date.fromisocalendar(year, week, 7)
