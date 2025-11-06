"""Scoring and recommendation heuristics for AktieTipset."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from data_integration.providers.base import Fundamental, Quote


@dataclass
class Recommendation:
    ticker: str
    score: float
    signal: str
    reasoning: list[str]


@dataclass
class IndicatorSnapshot:
    ticker: str
    sma_short: float | None = None
    sma_long: float | None = None
    rsi: float | None = None
    atr: float | None = None
    price_return: float | None = None


class RecommendationScorer:
    """Calculate scores, signals and reasoning based on technical/fundamental data."""

    def score(
        self,
        history: Mapping[str, Sequence[dict]],
        fundamentals: Sequence[Fundamental],
        quotes: Sequence[Quote],
        indicators: Mapping[str, IndicatorSnapshot],
    ) -> list[Recommendation]:
        fundamentals_map = {f.ticker: f for f in fundamentals}
        price_map = {quote.ticker: quote for quote in quotes}

        results: list[Recommendation] = []
        for ticker, candles in history.items():
            if not candles:
                continue

            latest_quote = price_map.get(ticker)
            fundamenta = fundamentals_map.get(ticker)
            indicator = indicators.get(ticker)

            score, reasoning = self._calculate_score(latest_quote, fundamenta, indicator)
            signal = self._derive_signal(score)

            results.append(Recommendation(ticker=ticker, score=score, signal=signal, reasoning=reasoning))
        return results

    def _calculate_score(
        self,
        quote: Quote | None,
        fundamenta: Fundamental | None,
        indicator: IndicatorSnapshot | None,
    ) -> tuple[float, list[str]]:
        score = 30.0  # baseline neutral score
        reasons: list[tuple[float, str]] = []

        if indicator:
            if indicator.sma_short is not None and indicator.sma_long is not None:
                trend_diff = indicator.sma_short - indicator.sma_long
                trend_score = max(min(trend_diff / indicator.sma_long * 25 if indicator.sma_long else 0, 20), -15)
                score += trend_score
                direction = "över" if trend_diff > 0 else "under"
                reasons.append((abs(trend_score), f"Kort trend {direction} lång trend"))

            if indicator.rsi is not None:
                rsi = indicator.rsi
                if 45 <= rsi <= 70:
                    rsi_score = 12
                elif 30 <= rsi < 45:
                    rsi_score = 6
                elif rsi < 30:
                    rsi_score = -10
                else:
                    rsi_score = -6
                score += rsi_score
                if rsi_score >= 0:
                    reasons.append((abs(rsi_score), f"RSI {rsi:.1f} (positivt momentum)"))
                else:
                    reasons.append((abs(rsi_score), f"RSI {rsi:.1f} signalerar svaghet"))

            if indicator.price_return is not None:
                momentum_score = max(min(indicator.price_return * 100, 15), -15)
                score += momentum_score
                change_pct = indicator.price_return * 100
                sentiment = "stigande" if momentum_score >= 0 else "fallande"
                reasons.append((abs(momentum_score), f"Pris {sentiment} {change_pct:.1f}%"))

            if indicator.atr is not None and quote and quote.price:
                atr_pct = indicator.atr / quote.price
                if atr_pct <= 0:
                    vol_score = 10
                elif atr_pct < 0.08:
                    vol_score = (0.08 - atr_pct) / 0.08 * 10
                else:
                    vol_score = -((atr_pct - 0.08) / 0.08 * 12)
                score += vol_score
                reasons.append((abs(vol_score), f"ATR {atr_pct * 100:.1f}% av priset"))

        if fundamenta:
            if fundamenta.pe_ratio is not None:
                if fundamenta.pe_ratio <= 18:
                    pe_score = 15
                elif fundamenta.pe_ratio <= 30:
                    pe_score = 8
                else:
                    pe_score = -10
                score += pe_score
                label = "attraktivt" if pe_score >= 0 else "högt"
                reasons.append((abs(pe_score), f"P/E {fundamenta.pe_ratio:.1f} {label}"))

            if fundamenta.roe is not None:
                roe_score = max(min(fundamenta.roe / 25 * 12, 12), -6)
                score += roe_score
                reasons.append((abs(roe_score), f"ROE {fundamenta.roe:.1f}%"))

            if fundamenta.debt_to_equity is not None:
                if fundamenta.debt_to_equity <= 0.5:
                    debt_score = 8
                elif fundamenta.debt_to_equity <= 1.0:
                    debt_score = 4
                else:
                    debt_score = -6
                score += debt_score
                reasons.append((abs(debt_score), f"Skuldgrad {fundamenta.debt_to_equity:.2f}"))

        score = max(0.0, min(score, 100.0))
        reasoning = [text for _, text in sorted(reasons, key=lambda item: item[0], reverse=True)[:3]]
        return score, reasoning

    def _derive_signal(self, score: float) -> str:
        if score >= 70:
            return "BUY"
        if score >= 50:
            return "ACCUMULATE"
        if score >= 40:
            return "HOLD"
        if score >= 30:
            return "TRIM"
        return "SELL"
