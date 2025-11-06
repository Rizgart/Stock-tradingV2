# Portföljuppföljning & Alerts

## Funktioner
- Import av innehav via CSV och API (Nordnet, Avanza m.fl.).
- Beräkning av P&L (realiserad/orealiserad), CAGR, beta, max drawdown.
- Alert-motor som stödjer prisnivåer, procentuella rörelser och indikator-korsningar.
- Tyst läge för att pausa notifieringar under angivna tidsfönster.

## Processflöde
1. **Import** – användaren laddar upp CSV eller kopplar API. Backend normaliserar poster och lagrar i PostgreSQL.
2. **Synk** – batchjobb uppdaterar kurser och räknar ut risk-/avkastningsmått.
3. **Alerts** – regler evalueras varje gång ny kursdata anländer eller enligt schema.
4. **Notiser** – skickas via in-app, desktop push och (valfritt) e-post.

## Datamodell (utkast)
- `portfolio_accounts`
- `portfolio_positions`
- `portfolio_transactions`
- `alert_rules`
- `alert_events`

## Nyckeltal
- **Beta**: jämförelse mot valt index (t.ex. OMX30 eller S&P 500).
- **Max Drawdown**: spåras via rullande topp/botten.
- **Volatilitet (ATR)**: används för alerttrösklar.
- **Sharpe Ratio**: räknas i backtesting/rapport.

## Notifieringsmotor
- Eventdriven (t.ex. med Kafka eller Redis Streams) eller schemalagd via Celery.
- Rate limiting per användare för att undvika spam.
- Loggning och audit av skickade notifieringar.
