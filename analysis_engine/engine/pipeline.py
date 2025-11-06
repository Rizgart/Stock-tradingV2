"""Pipeline för att driva analysflödet."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from data_integration.providers.base import MarketDataProvider

from .indicators import calculate_atr, calculate_return, calculate_rsi, calculate_sma
from .scoring import IndicatorSnapshot, Recommendation, RecommendationScorer


@dataclass
class PipelineConfig:
    tickers: list[str]
    start: datetime
    end: datetime
    interval: str = "1d"


class AnalysisPipeline:
    """Kopplar samman datahämtning och scoring."""

    def __init__(
        self,
        provider: MarketDataProvider,
        scorer: RecommendationScorer,
        config: PipelineConfig,
    ) -> None:
        self.provider = provider
        self.scorer = scorer
        self.config = config

    def run(self) -> list[Recommendation]:
        """Kör pipeline och returnera rekommendationer."""

        history = {
            ticker: self.provider.get_history(
                ticker,
                start=self.config.start,
                end=self.config.end,
                interval=self.config.interval,
            )
            for ticker in self.config.tickers
        }
        fundamentals = self.provider.get_fundamentals(self.config.tickers)
        quotes = self.provider.get_quotes(self.config.tickers)

        indicators = {
            ticker: IndicatorSnapshot(
                ticker=ticker,
                sma_short=calculate_sma(candles, 20),
                sma_long=calculate_sma(candles, 50),
                rsi=calculate_rsi(candles, 14),
                atr=calculate_atr(candles, 14),
                price_return=calculate_return(candles, 5),
            )
            for ticker, candles in history.items()
        }

        return self.scorer.score(
            history=history,
            fundamentals=fundamentals,
            quotes=quotes,
            indicators=indicators,
        )
