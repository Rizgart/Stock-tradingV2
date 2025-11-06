from datetime import UTC, datetime, timedelta

from analysis_engine.engine.indicators import calculate_atr, calculate_return, calculate_rsi, calculate_sma


def _build_candles() -> list[dict[str, float | str]]:
    base = datetime.now(UTC) - timedelta(days=10)
    candles = []
    price = 100.0
    for index in range(15):
        timestamp = base + timedelta(days=index)
        high = price * 1.02
        low = price * 0.98
        close = price * 1.01
        candles.append({
            "open": price,
            "high": high,
            "low": low,
            "close": close,
            "volume": 1_000_000 + index * 1000,
            "timestamp": timestamp.isoformat(),
        })
        price = close
    return candles


def test_calculate_sma_returns_value() -> None:
    candles = _build_candles()
    value = calculate_sma(candles, 5)
    assert value is not None
    assert value > 0


def test_calculate_rsi_in_range() -> None:
    candles = _build_candles()
    value = calculate_rsi(candles, 14)
    assert value is None or 0 <= value <= 100


def test_calculate_atr_positive() -> None:
    candles = _build_candles()
    value = calculate_atr(candles, 14)
    assert value is not None
    assert value > 0


def test_calculate_return_positive() -> None:
    candles = _build_candles()
    value = calculate_return(candles, 5)
    assert value is not None
    assert value > 0
