from __future__ import annotations

import uvicorn

from app.config import settings


def main() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.port, reload=settings.env == "development")


if __name__ == "__main__":
    main()
