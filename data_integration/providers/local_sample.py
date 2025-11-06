"""Local in-memory data provider used for development and testing."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from random import Random
from typing import Iterable

from .base import AbstractMarketDataProvider, Fundamental, Quote


class LocalSampleProvider(AbstractMarketDataProvider):
    """Generate deterministic mock data when external APIs are unavailable."""

    def __init__(self) -> None:
        self._rng = Random(42)
        self._base_quotes: dict[str, Quote] = {}
        self._fundamentals: dict[str, Fundamental] = {
            "AAPL": Fundamental(ticker="AAPL", pe_ratio=24.5, ps_ratio=6.2, roe=32.1, debt_to_equity=0.55),
            "TSLA": Fundamental(ticker="TSLA", pe_ratio=55.0, ps_ratio=7.5, roe=15.3, debt_to_equity=0.35),
            "ERIC": Fundamental(ticker="ERIC", pe_ratio=16.2, ps_ratio=1.8, roe=11.4, debt_to_equity=0.42),
        }

    def _quote_for(self, ticker: str) -> Quote:
        quote = self._base_quotes.get(ticker)
        if quote:
            return quote
        price = {
            "AAPL": 189.3,
            "TSLA": 182.4,
            "ERIC": 72.8,
        }.get(ticker.upper(), 120.0)
        quote = Quote(ticker=ticker.upper(), price=price, currency="USD", timestamp=datetime.now(UTC))
        self._base_quotes[ticker.upper()] = quote
        return quote

    def get_quotes(self, tickers: Iterable[str]) -> list[Quote]:  # type: ignore[override]
        return [self._quote_for(ticker) for ticker in tickers]

    def get_history(  # type: ignore[override]
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        interval: str = "1d",
    ) -> list[dict]:
        if interval not in {"1d", "1h"}:
            raise ValueError("Unsupported interval")

        step = timedelta(days=1) if interval == "1d" else timedelta(hours=1)
        candles: list[dict] = []
        quote = self._quote_for(ticker)
        span = int((end - start) / step)
        price = quote.price
        for index in range(max(span, 30)):
            timestamp = start + step * index
            drift = self._rng.uniform(-0.015, 0.02)
            high = price * (1 + max(drift, 0) + 0.01)
            low = price * (1 + min(drift, 0) - 0.01)
            close = max(1.0, price * (1 + drift))
            open_price = price
            volume = int(1_000_000 + self._rng.random() * 500_000)
            candles.append(
                {
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(close, 2),
                    "volume": volume,
                    "timestamp": timestamp.isoformat(),
                }
            )
            price = close
        return candles

    def get_fundamentals(self, tickers: Iterable[str]) -> list[Fundamental]:  # type: ignore[override]
        results: list[Fundamental] = []
        for ticker in tickers:
            fundamental = self._fundamentals.get(ticker.upper())
            if fundamental:
                results.append(fundamental)
            else:
                results.append(
                    Fundamental(
                        ticker=ticker.upper(),
                        pe_ratio=28.0,
                        ps_ratio=4.5,
                        roe=12.0,
                        debt_to_equity=0.75,
                    )
                )
        return results

    def search_ticker(self, query: str) -> list[dict]:  # type: ignore[override]
        return [
            {"ticker": ticker, "name": ticker, "source": "local"}
            for ticker in self._fundamentals
            if query.lower() in ticker.lower()
        ]
