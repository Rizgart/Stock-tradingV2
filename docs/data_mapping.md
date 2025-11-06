# Data Mapping – Massive API till StockEntity

Detta dokument beskriver hur data från Massive API mappas till interna modeller i AktieTipset.

## Input
- Källa: `GET /v3/reference/tickers`
- Autentisering: API-nyckel via header `Authorization: Bearer <token>`

## Fältmappning
| Massive fält | Typ | Beskrivning | Intern mappning |
| ------------ | --- | ----------- | --------------- |
| `ticker` | string | Kortnamn på aktie | `StockEntity.ticker` (primärnyckel) |
| `name` | string | Bolagsnamn | `StockEntity.name` |
| `market` | string | Marknadstyp | `StockEntity.market` |
| `locale` | string | Region | `StockEntity.locale` |
| `primary_exchange` | string | Börskod | `StockEntity.exchange` |
| `type` | string | Instrumenttyp | `StockEntity.instrument_type` |
| `active` | boolean | Om instrumentet är aktivt | `StockEntity.is_active` |
| `currency_name` | string | Valuta | `StockEntity.currency` |
| `cik` | string | SEC-identifierare | `StockEntity.cik` |
| `composite_figi` | string | Global FIGI | `StockEntity.composite_figi` |
| `share_class_figi` | string | FIGI för aktieklass | `StockEntity.share_class_figi` |
| `last_updated_utc` | datetime | Senaste uppdatering | `StockEntity.last_updated` (ISO8601 UTC) |

## Identifieringslogik
1. Primärt: `ticker`
2. Sekundärt: `composite_figi`
3. Tertiärt: `cik`

## Normalisering
- Trimma whitespace och säkerställ `A–Z0–9` i ticker.
- Konvertera datumfält till `datetime` (UTC, ISO8601).
- Hantera valutaomvandling baserat på användarens profil.

## Berikning
Efter grundmappningen enrichas `StockEntity` med:
- Historisk prisdata (`/market/history/{ticker}`)
- Bolagsdata (sektor, bransch, land)
- Analysresultat (trend, fundamenta, sentiment)

## Pipeline
1. `fetch_api_data`
2. `validate_schema`
3. `transform_to_internal_model`
4. `enrich_with_marketdata`
5. `score_and_rank`
6. `persist_to_local_cache`

## Exempeloutput
```json
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "market": "stocks",
  "exchange": "XNAS",
  "currency": "USD",
  "active": true,
  "last_updated": "2025-11-06T07:05:49Z",
  "score": 87,
  "signal": "BUY",
  "reasoning": ["Stark momentum", "Låg volatilitet", "Positiv vinsttrend"]
}
```
