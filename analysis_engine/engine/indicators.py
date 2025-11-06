"""Utilities for calculating technical indicators used in scoring."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence


def _timestamp_key(candle: dict[str, Any]) -> float:
    ts = candle.get("timestamp")
    if isinstance(ts, (int, float)):
        return float(ts)
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return 0.0
    if isinstance(ts, datetime):
        return ts.timestamp()
    return 0.0


def _prepare_series(candles: Sequence[dict[str, Any]]) -> tuple[list[float], list[float], list[float]]:
    sorted_candles = sorted(candles, key=_timestamp_key)
    closes: list[float] = []
    highs: list[float] = []
    lows: list[float] = []
    for candle in sorted_candles:
        close = _to_float(candle.get("close"))
        high = _to_float(candle.get("high", close))
        low = _to_float(candle.get("low", close))
        if close is None or high is None or low is None:
            continue
        closes.append(close)
        highs.append(high)
        lows.append(low)
    return closes, highs, lows


def _to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def calculate_sma(candles: Sequence[dict[str, Any]], period: int) -> float | None:
    """Return a simple moving average for the supplied period."""

    if period <= 0:
        raise ValueError("period must be positive")
    closes, _, _ = _prepare_series(candles)
    if not closes:
        return None
    window = closes[-period:] if len(closes) >= period else closes
    return sum(window) / len(window)


def calculate_rsi(candles: Sequence[dict[str, Any]], period: int = 14) -> float | None:
    """Calculate the Relative Strength Index (RSI)."""

    if period <= 0:
        raise ValueError("period must be positive")
    closes, _, _ = _prepare_series(candles)
    if len(closes) <= period:
        return None
    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(closes, closes[1:]):
        change = current - previous
        if change > 0:
            gains.append(change)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(change))
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))


def calculate_atr(candles: Sequence[dict[str, Any]], period: int = 14) -> float | None:
    """Average True Range (ATR) as volatility proxy."""

    if period <= 0:
        raise ValueError("period must be positive")
    closes, highs, lows = _prepare_series(candles)
    if len(closes) <= period:
        return None
    true_ranges: list[float] = []
    for index in range(1, len(closes)):
        high = highs[index]
        low = lows[index]
        prev_close = closes[index - 1]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        true_ranges.append(tr)
    if len(true_ranges) < period:
        period_range = true_ranges
    else:
        period_range = true_ranges[-period:]
    if not period_range:
        return None
    return sum(period_range) / len(period_range)


def calculate_return(candles: Sequence[dict[str, Any]], lookback: int = 1) -> float | None:
    """Price return over the specified number of last periods."""

    if lookback <= 0:
        raise ValueError("lookback must be positive")
    closes, _, _ = _prepare_series(candles)
    if len(closes) <= lookback:
        return None
    recent = closes[-1]
    previous = closes[-(lookback + 1)]
    if previous == 0:
        return None
    return (recent - previous) / previous
