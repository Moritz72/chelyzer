from fastapi import APIRouter

from chelyzer_api.enums import Opening

options_router = APIRouter(prefix="/options", tags=["options"])


@options_router.get("/opening", response_model=list[str])
def get_openings() -> list[str]:
    """Return all available openings."""
    return [opening.value for opening in Opening]
