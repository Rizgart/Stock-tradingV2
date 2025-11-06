"""FastAPI dependency wiring for the analysis engine service."""

from __future__ import annotations

import os
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from analysis_engine.engine.pipeline import AnalysisPipeline, PipelineConfig
from analysis_engine.engine.scoring import RecommendationScorer
from data_integration.providers.base import MarketDataProvider
from data_integration.providers.local_sample import LocalSampleProvider

try:
    from data_integration.providers.massive_api import MassiveAPIProvider  # type: ignore[attr-defined]
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    MassiveAPIProvider = None  # type: ignore[assignment]

DEFAULT_TICKERS = ["AAPL", "TSLA", "ERIC"]
DEFAULT_LOOKBACK_DAYS = 120


def get_market_data_provider() -> MarketDataProvider:
    api_key = os.environ.get("MASSIVE_API_KEY")
    if api_key:
        if MassiveAPIProvider is None:
            raise RuntimeError("MassiveAPIProvider kräver httpx-biblioteket installerat")
        return MassiveAPIProvider(api_key=api_key)  # type: ignore[call-arg]
    return LocalSampleProvider()


@lru_cache(maxsize=1)
def get_scorer() -> RecommendationScorer:
    return RecommendationScorer()


def get_pipeline(
    provider: Annotated[MarketDataProvider, Depends(get_market_data_provider)],
    scorer: Annotated[RecommendationScorer, Depends(get_scorer)],
) -> AnalysisPipeline:
    end = datetime.now(UTC)
    start = end - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    config = PipelineConfig(tickers=DEFAULT_TICKERS, start=start, end=end, interval="1d")
    return AnalysisPipeline(provider=provider, scorer=scorer, config=config)
