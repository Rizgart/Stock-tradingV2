"""Klient för kommunikation med analysmotorn."""

from __future__ import annotations

from typing import Protocol

import httpx


class AnalysisClient(Protocol):
    """Gränssnitt för att hämta data från analysmotorn."""

    def fetch_recommendations(self) -> list[dict]:
        """Hämta aktuella rekommendationer."""


class HttpAnalysisClient:
    """HTTP-implementering mot analysmotorns REST-endpoints."""

    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=timeout)

    def fetch_recommendations(self) -> list[dict]:  # type: ignore[override]
        response = self._client.get(f"{self.base_url}/recommendations")
        response.raise_for_status()
        return response.json().get("results", [])


def get_analysis_client() -> HttpAnalysisClient:
    """Dependency som kan overridas i tester."""

    return HttpAnalysisClient(base_url="http://localhost:9000")
