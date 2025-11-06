"""Adapter mot Massive API."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import httpx

from .base import AbstractMarketDataProvider, Fundamental, MarketDataProvider, Quote


class MassiveAPIProvider(AbstractMarketDataProvider):
    """REST-baserad integration mot Massive API."""

    def __init__(self, api_key: str, base_url: str = "https://api.massive.com/v3") -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=10.0)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def get_quotes(self, tickers: Iterable[str]) -> list[Quote]:  # type: ignore[override]
        symbols = ",".join(sorted({ticker.upper() for ticker in tickers}))
        if not symbols:
            return []
        url = f"{self.base_url}/market/quotes"
        response = self._client.get(url, params={"symbols": symbols}, headers=self._headers())
        response.raise_for_status()
        payload = response.json().get("results", [])
        quotes: list[Quote] = []
        for item in payload:
            quotes.append(
                Quote(
                    ticker=item["symbol"],
                    price=float(item["lastPrice"]),
                    currency=item.get("currency", "USD"),
                    timestamp=datetime.fromisoformat(item["updatedUtc"].replace("Z", "+00:00")),
                )
            )
        return quotes

    def get_history(  # type: ignore[override]
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        interval: str = "1d",
    ) -> list[dict]:
        url = f"{self.base_url}/market/history/{ticker.upper()}"
        params = {
            "start": start.isoformat(),
            "end": end.isoformat(),
            "interval": interval,
        }
        response = self._client.get(url, params=params, headers=self._headers())
        response.raise_for_status()
        return response.json().get("results", [])

    def get_fundamentals(self, tickers: Iterable[str]) -> list[Fundamental]:  # type: ignore[override]
        symbols = ",".join(sorted({ticker.upper() for ticker in tickers}))
        if not symbols:
            return []
        url = f"{self.base_url}/fundamentals/summary"
        response = self._client.get(url, params={"symbols": symbols}, headers=self._headers())
        response.raise_for_status()
        payload = response.json().get("results", [])
        fundamentals: list[Fundamental] = []
        for item in payload:
            fundamentals.append(
                Fundamental(
                    ticker=item["symbol"],
                    pe_ratio=_safe_float(item.get("peRatio")),
                    ps_ratio=_safe_float(item.get("psRatio")),
                    roe=_safe_float(item.get("roe")),
                    debt_to_equity=_safe_float(item.get("debtToEquity")),
                )
            )
        return fundamentals

    def search_ticker(self, query: str) -> list[dict]:  # type: ignore[override]
        url = f"{self.base_url}/reference/tickers"
        response = self._client.get(
            url,
            params={"search": query, "limit": 20, "order": "asc", "sort": "ticker"},
            headers=self._headers(),
        )
        response.raise_for_status()
        return response.json().get("results", [])


def _safe_float(value: object | None) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None
