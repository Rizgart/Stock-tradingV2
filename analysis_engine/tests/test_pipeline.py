from datetime import UTC, datetime, timedelta

from analysis_engine.engine.pipeline import AnalysisPipeline, PipelineConfig
from analysis_engine.engine.scoring import RecommendationScorer
from data_integration.providers.local_sample import LocalSampleProvider


def test_pipeline_run_returns_recommendations() -> None:
    provider = LocalSampleProvider()
    scorer = RecommendationScorer()
    end = datetime.now(UTC)
    start = end - timedelta(days=60)
    config = PipelineConfig(tickers=["AAPL", "TSLA"], start=start, end=end, interval="1d")
    pipeline = AnalysisPipeline(provider=provider, scorer=scorer, config=config)

    results = pipeline.run()

    assert results
    assert all(recommendation.reasoning for recommendation in results)
