from datetime import UTC, datetime, timedelta

from data_integration.providers.base import Fundamental, Quote
from analysis_engine.engine.scoring import IndicatorSnapshot, RecommendationScorer


def test_recommendation_scoring_generates_reasoning() -> None:
    scorer = RecommendationScorer()
    now = datetime.now(UTC)
    history = {
        "AAPL": [
            {"close": 150.0, "timestamp": (now - timedelta(days=5)).isoformat()},
            {"close": 152.0, "timestamp": (now - timedelta(days=4)).isoformat()},
            {"close": 154.0, "timestamp": (now - timedelta(days=3)).isoformat()},
            {"close": 156.0, "timestamp": (now - timedelta(days=2)).isoformat()},
            {"close": 160.0, "timestamp": (now - timedelta(days=1)).isoformat()},
            {"close": 165.0, "timestamp": now.isoformat()},
        ]
    }
    fundamentals = [Fundamental(ticker="AAPL", pe_ratio=22.0, roe=18.0, debt_to_equity=0.45)]
    quotes = [Quote(ticker="AAPL", price=168.0, currency="USD", timestamp=now)]
    indicators = {
        "AAPL": IndicatorSnapshot(
            ticker="AAPL",
            sma_short=158.0,
            sma_long=150.0,
            rsi=58.0,
            atr=4.5,
            price_return=0.08,
        )
    }

    results = scorer.score(history=history, fundamentals=fundamentals, quotes=quotes, indicators=indicators)

    assert results
    recommendation = results[0]
    assert recommendation.ticker == "AAPL"
    assert recommendation.score > 0
    assert len(recommendation.reasoning) <= 3
