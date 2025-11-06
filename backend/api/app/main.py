"""FastAPI-ingångspunkt för AktieTipset backend."""

from __future__ import annotations

from fastapi import FastAPI

from .routers import recommendations

app = FastAPI(
    title="AktieTipset API",
    version="0.1.0",
    description=(
        "Backend-API för AktieTipset. Tillhandahåller marknadsdata, rekommendationer, "
        "portföljhantering och notifieringar."
    ),
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health endpoint för övervakning."""

    return {"status": "ok"}


app.include_router(recommendations.router)
