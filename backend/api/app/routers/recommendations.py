"""Endpointdefinitioner för rekommendationer."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from ..analysis_client import AnalysisClient, get_analysis_client

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/", summary="Hämta rekommendationer")
def list_recommendations(
    client: Annotated[AnalysisClient, Depends(get_analysis_client)],
) -> dict[str, list[dict]]:
    """Returnera aktuella rekommendationer från analysmotorn."""

    recommendations = client.fetch_recommendations()
    return {"results": recommendations}
