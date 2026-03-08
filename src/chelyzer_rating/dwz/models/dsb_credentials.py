from pydantic import BaseModel


class DsbCredentials(BaseModel):
    """Model for credentials for the Deutscher Schachbund."""

    username: str
    password: str
