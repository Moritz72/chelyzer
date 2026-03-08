import uvicorn

from chelyzer_api.app import create_app


def launch() -> None:
    """Launch a new app instance."""
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104


if __name__ == "__main__":
    launch()
