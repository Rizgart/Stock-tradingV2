from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query

from analysis_engine.engine.pipeline import AnalysisPipeline, PipelineConfig
from analysis_engine.engine.scoring import Recommendation

from .dependencies import DEFAULT_TICKERS, get_pipeline

app = FastAPI(
    title="AktieTipset Analysis Engine",
    version="0.2.0",
    description=(
        "Analysmotor som kombinerar tekniska indikatorer och fundamentala datapunkter "
        "för att generera rankningar och rekommendationer."
    ),
)

DISCLAIMER = (
    "Rekommendationerna är endast för informations- och utbildningssyfte och ska inte uppfattas "
    "som finansiell rådgivning. Historisk avkastning är ingen garanti för framtida resultat."
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


def _parse_tickers(tickers: str | None) -> list[str]:
    if not tickers:
        return DEFAULT_TICKERS
    parsed = [ticker.strip().upper() for ticker in tickers.split(",") if ticker.strip()]
    if not parsed:
        raise HTTPException(status_code=400, detail="Minst en ticker måste anges")
    return parsed


@app.get("/recommendations", tags=["recommendations"])
def get_recommendations(
    tickers: Annotated[str | None, Query(description="Kommaseparerad lista av tickers")] = None,
    lookback_days: Annotated[int, Query(ge=5, le=365, description="Antal dagar att analysera")] = 120,
    interval: Annotated[str, Query(pattern="^(1d|1h)$", description="Aggregeringsintervall")] = "1d",
    pipeline: Annotated[AnalysisPipeline, Depends(get_pipeline)],
) -> dict[str, object]:
    requested_tickers = _parse_tickers(tickers)
    end = datetime.now(UTC)
    start = end - timedelta(days=lookback_days)
    pipeline.config = PipelineConfig(tickers=requested_tickers, start=start, end=end, interval=interval)

    recommendations: list[Recommendation] = pipeline.run()
    payload = [
        {
            "ticker": recommendation.ticker,
            "score": recommendation.score,
            "signal": recommendation.signal,
            "reasoning": recommendation.reasoning,
        }
        for recommendation in recommendations
    ]
    return {
        "generatedAt": datetime.now(UTC).isoformat(),
        "disclaimer": DISCLAIMER,
        "results": payload,
    }
