# Analysmotor

Analysmotorn ansvarar för att hämta data, beräkna indikatorer och generera rankingar och rekommendationer. Modulen körs som en separat tjänst (REST eller gRPC) och kommunicerar med backend-API:t.

## Delkomponenter
- **Pipelines** för att hämta och transformera data.
- **Indikatorer** för teknisk analys (MA, MACD, RSI, ATR).
- **Fundamental analys** för att räkna ut P/E, P/S, ROE, skuldgrad m.m.
- **Ranking & Explainability** för att producera score och topp 3 motiveringar.
- **Backtesting** för att utvärdera strategier över flera tidsperioder.

## Utveckling
Se `requirements.txt` för beroenden och kör `pytest` för att validera pipeline-moduler.
## Köra tjänsten

```bash
uvicorn analysis_engine.app.main:app --reload
```

API:t exponeras på `http://localhost:8000` och levererar rekommendationer via `/recommendations`.

## Testning

```bash
pytest analysis_engine
```

