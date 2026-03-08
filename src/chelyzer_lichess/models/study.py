from pydantic import BaseModel, Field


class Study(BaseModel):
    """Model for a lichess study."""

    id: str
    name: str
    created_at: int = Field(..., alias="createdAt")
    updated_at: int = Field(..., alias="updatedAt")

    def is_ignored(self) -> bool:
        """Return whether the study is to be ignored."""
        return self.name.endswith("# chelyzer: ignore")
