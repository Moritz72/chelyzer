from datetime import date

from sqlmodel import Field, Index, SQLModel, desc


class PlayerDwz(SQLModel, table=True):
    """Model for a player DWZ entry at a certain date."""

    __table_args__ = (Index("ix_name_date", "name", desc("list_date")),)

    name: str = Field(primary_key=True)
    birthyear: int = Field(primary_key=True)
    list_date: date = Field(primary_key=True)
    dwz: int
