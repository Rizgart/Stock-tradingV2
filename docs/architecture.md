# Systemarkitektur – AktieTipset

Detta dokument beskriver arkitektur, moduler och teknikval för AktieTipset.

## Översikt

AktieTipset följer en modulär mikrotjänst-arkitektur:

- **Frontend (desktop)** – React + Tauri. Renderar UI och interagerar med lokala resurser (Keychain/DPAPI, filsystem). Kommunicerar med backend via REST/gRPC.
- **Backend API** – FastAPI som exponerar REST-endpoints för autentisering, datakonsumtion, notifieringar och administration.
- **Analysmotor** – Fristående Python-tjänst som kör teknisk/fundamental analys, ranking och backtesting.
- **Data Integration Layer** – Adapterlager mot externa marknadsdatakällor (Massive API m.fl.) med caching och rate-limit-hantering.
- **Data Store** – Lokal SQLite-cache + moln-PostgreSQL för persistens, historik och användarsynk.

```
Frontend (Tauri) <-> Backend API (FastAPI) <-> Analysis Engine (FastAPI/gRPC)
                             |
                             +--> Data Integration (Massive API, Nordnet, ...)
                             |
                             +--> PostgreSQL / SQLite
```

## Modulbeskrivning

### Frontend – Desktop (React + Tauri)
- **State Management:** Redux Toolkit + RTK Query för datafetching.
- **UI-kit:** Mantine eller Chakra UI med stöd för mörkt/kontrastläge.
- **Internationalisering:** `react-i18next` med sv/en-översättningar.
- **Notiser:** Electron/Tauri notification API + e-post via backend.
- **Nyckelvy**: Dashboard, rekommendationer, aktiedetaljer, watchlist/portfölj, inställningar.

### Backend API (FastAPI)
- **Autentisering:** OAuth2 med API-nycklar/tokenlagring. Lokala tokens krypteras med OS-keychain.
- **API-ytor:**
  - `/auth/api-key` – hantera API-nycklar.
  - `/market` – proxade data från datalagret.
  - `/recommendations` – exponera rankingar och förklaringar.
  - `/portfolio` – import, P&L, alerts.
  - `/notifications` – schema och tyst läge.
- **Bakgrundsjobb:** `APScheduler` eller `Celery` (med Redis) för batchjobb och notifieringar.
- **Rate limiting & caching:** `fastapi-cache2` + Redis/SQLite.

### Analysmotor
- **Pipelines:**
  1. `fetch_api_data` – hämta data via `MarketDataProvider`.
  2. `validate_schema` – säkerställ datakvalitet.
  3. `transform_to_internal_model` – normalisera & mappa till `StockEntity`.
  4. `enrich_with_marketdata` – komplettera sektor, fundamenta, sentiment.
  5. `score_and_rank` – beräkna indikatorer, fundamentalpoäng och riskscore.
  6. `persist_to_local_cache` – skriv till SQLite/Redis.
- **Moduler:**
  - `indicators` – MA, MACD, RSI, ATR m.fl.
  - `fundamentals` – beräkna P/E, P/S, ROE, skuldgrad.
  - `ranking` – ensemble som väger tekniska och fundamentala signaler, genererar score 0–100 samt signal (BUY/HOLD/SELL).
  - `explainability` – presenterar topp 3 faktorer per rekommendation.
  - `backtesting` – walk-forward, out-of-sample tester med mått CAGR, Sharpe, MaxDD, WinRate.

### Data Integration Layer
- **Interface:** `MarketDataProvider` (dataklasser i `data_integration/providers/base.py`).
- **Implementering:** `MassiveAPIProvider` (REST), framtida adaptors för Nordnet, Yahoo Finance m.fl.
- **Caching:** kombination av in-memory (Redis) och lokal SQLite. TTL 15–60s intraday, 24h EOD.
- **Rate limiting:** Token bucket med exponential backoff.

### Datahantering
- **Lokalt:** SQLite via `sqlmodel` för caching och offline-mode.
- **Fjärr:** PostgreSQL (via SQLAlchemy) för användare, portföljer, historik, loggar.
- **Schema:** `StockEntity` innehåller identifierare (ticker, FIGI, CIK), metadata, senaste score/signal och motivering.

### Säkerhet
- All kommunikation skyddas med TLS.
- Tokenlagring sker krypterat via OS keychain (macOS Keychain / Windows DPAPI).
- API-nycklar maskeras i UI och loggar.
- GDPR-processer: samtycke, rätten att bli glömd, dataminimering.
- MiFID-disclaimer visas vid onboarding och i rapporter.

## Deployment & DevOps
- **Miljöer:** Dev, Beta, Prod. Feature toggles med LaunchDarkly eller eget system.
- **CI/CD:** GitHub Actions med pipelines för lint, test, build (frontend/backend), backtesting regression.
- **Paketering:**
  - macOS: Notarized DMG via Tauri bundler.
  - Windows: MSIX/EXE med signerade builds.
- **Monitoring:** Prometheus/Grafana för backend och analysmotor, Sentry för frontend.

## Skalning & framtida expansion
- Containerisering med Docker för backend och analysmotor.
- Kubernetes (EKS/AKS) för skalning och jobbhantering.
- ML-pipeline för prediktiva signaler (t.ex. scikit-learn, PyTorch) via separata tjänster.
- Eventdriven arkitektur (Kafka) för realtidsuppdateringar och notifieringar.

## Teknologistack (sammanfattning)

| Lager | Teknologier |
| ----- | ----------- |
| Frontend | React, Tauri, TypeScript, Redux Toolkit, Mantine/Chakra, i18next |
| Backend | FastAPI, SQLModel, Celery/APScheduler, Redis, PostgreSQL |
| Analys | pandas, numpy, scikit-learn, ta-lib, statsmodels |
| DevOps | GitHub Actions, Docker, Kubernetes, Sentry, Prometheus |

## Öppna frågor
- Val av UI-bibliotek (Mantine vs Chakra) behöver beslutas.
- Val av notifieringskanal för e-post (SendGrid, AWS SES, etc.).
- Lagring av sentimentdata (extern API? egen ML-modell?).
