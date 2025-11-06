"""Definition av gränssnittet för dataleverantörer."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol


@dataclass
class Quote:
    ticker: str
    price: float
    currency: str
    timestamp: datetime


@dataclass
class Fundamental:
    ticker: str
    pe_ratio: float | None = None
    ps_ratio: float | None = None
    roe: float | None = None
    debt_to_equity: float | None = None


class MarketDataProvider(Protocol):
    """Abstrakt gränssnitt för externa dataleverantörer."""

    def get_quotes(self, tickers: Iterable[str]) -> list[Quote]:
        """Hämta senaste quotes för givna tickers."""

    def get_history(
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        interval: str = "1d",
    ) -> list[dict]:
        """Returnera historisk OHLC-data."""

    def get_fundamentals(self, tickers: Iterable[str]) -> list[Fundamental]:
        """Returnera fundamentala nyckeltal."""

    def search_ticker(self, query: str) -> list[dict]:
        """Sök tickers baserat på fritext."""


class AbstractMarketDataProvider(abc.ABC):
    """Bas-klass som implementeringar kan ärva."""

    @abc.abstractmethod
    def get_quotes(self, tickers: Iterable[str]) -> list[Quote]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_history(
        self,
        ticker: str,
        start: datetime,
        end: datetime,
        interval: str = "1d",
    ) -> list[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_fundamentals(self, tickers: Iterable[str]) -> list[Fundamental]:
        raise NotImplementedError

    @abc.abstractmethod
    def search_ticker(self, query: str) -> list[dict]:
        raise NotImplementedError
