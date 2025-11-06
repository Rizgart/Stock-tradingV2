# Produktkrav – AktieTipset

Detta dokument sammanfattar funktions- och produktkraven för AktieTipset baserat på beställarens specifikation.

## Appinformation
- **Namn:** AktieTipset
- **Beskrivning:** Desktop-app som analyserar aktier och ger köprekommendationer med framtida stöd för iOS/Android.
- **Språk:** Svenska och engelska.

## Plattformar
- **Desktop:** macOS (Intel & Apple Silicon), Windows 10/11 (x64)
- **Mobil roadmap:** iOS (Universal), Android

## Kärnfunktioner
1. Rekommendationslista över aktier att köpa.
2. Teknisk och fundamental analys med motivering.
3. Löpande uppdateringar av kursdata.
4. Watchlist och portfölj med notifieringar.
5. Sök- och filterfunktion (bransch, marknad, P/E, volatilitet m.m.).
6. Favoriter, bevakningslistor och notiser.
7. Export av rapporter (PDF/CSV).

## Analysmotor
- **Datatyper:** OHLC + volym, nyheter/sentiment, bolagsnyckeltal (P/E, P/S, ROE, skuldgrad), marknadsindex & sektorjämförelser.
- **Teknisk analys:** Trend (MA, MACD, RSI), momentum/breakout, volatilitet (ATR).
- **Fundamental analys:** Värdering vs historik, tillväxt & lönsamhet.
- **Rankingmodell:** kombinerar tekniska signaler, fundamenta, risk/volatilitet och likviditet till score 0–100 samt köp/behåll/sälj.
- **Förklarbarhet:** Visa topp 3 faktorer för varje rekommendation.
- **Frekvens:** live-uppdatering vid ny kurspost samt daglig batch efter börsstängning.
- **Begränsning:** Tydlig disclaimer om att inga råd lämnas.

## Dataintegration
- **Primär API-källa:** Massive API (exempel-endpoint `/v3/reference/tickers`).
- **Sekundära källor:** Nordnet, Yahoo Finance, Alpha Vantage, Euronext Nasdaq Nordics.
- **Krav:** OAuth2/nyckelhantering, rate limit & caching, retrys & backoff.
- **Adaptergränssnitt:** `MarketDataProvider` med metoderna `get_quotes`, `get_history`, `get_fundamentals`, `search_ticker`.
- **Caching:** In-memory + lokal SQLite, TTL 15–60s (intraday) och 24h (EOD).

## Portföljuppföljning
- Importera innehav (CSV/API).
- P&L, avkastning, riskmått (beta, max drawdown).
- Alert-regler (prisnivå, procent, indikator-korsning) med tyst läge.
- Notiser via in-app, desktop push och ev. e-post.

## UI/UX
- **Vylista:** Dashboard, rekommendationer, aktiedetalj, watchlist/portfölj, inställningar.
- **Tillgänglighet:** tangentbordsnavigering, kontrastläge, justerbar textstorlek.

## Säkerhet & integritet
- Lagra tokens krypterat lokalt (Keychain/DPAPI).
- Kryptering at-rest och in-transit (TLS).
- GDPR-efterlevnad, MiFID-disclaimer.

## Arkitektur
- **Frontend desktop:** React + Tauri (TypeScript).
- **Mobil:** React Native (TypeScript) – delar komponenter.
- **Backend API:** FastAPI (Python).
- **Analysmotor:** Python (FastAPI/gRPC), libs `pandas`, `numpy`, `scikit-learn`, `ta-lib`.
- **Databaser:** Lokal SQLite (cache), fjärr PostgreSQL.
- **Kommunikation:** REST eller gRPC mellan backend och analys.
- **Arkitekturmönster:** Modulär mikrotjänst-arkitektur.
- **Expansion:** Cloud (AWS/Azure), ML-pipeline för prediktiva signaler.

## Prestanda
- Uppstartstid < 1.5s.
- Graf-rendering < 120ms.
- Max minne 400 MB.
- Hantera miljontals datapunkter via nedsampling.

## Kvalitet & test
- Enhetstester ≥80% täckning av kärnlogik.
- E2E för import, ranking och alerts.
- Backtesting över 6m, 1y, 3y, 5y, 10y med mått CAGR, Sharpe, MaxDD, WinRate. Walk-forward & out-of-sample.

## Distribution
- Paketering: MSIX/EXE för Windows, DMG (notarized) för macOS.
- Auto-uppdateringar med signering.
- Miljöer: Dev, Beta, Prod.

## Juridisk disclaimer
> Appen ger informations- och utbildningssyfte, ej personlig finansiell rådgivning. Historisk avkastning garanterar ej framtida resultat.

## Roadmap
- **MVP:** Realtidsdata, tekniska signaler, ranking med förklaringar, watchlist + notiser, Massive API-integration.
- **v1.1:** Fundamentalanalys & sektormodeller, portföljimport & P&L.
- **v1.2:** Nyheter/sentiment, PDF-export.
- **Mobile pilot:** Läs-läge med watchlist och pushnotiser.

## Acceptanskriterier
- Användare kan koppla API-nyckel och se kurser inom 1 minut.
- Minst 3 tekniska och 3 fundamentala nyckeltal i ranking.
- Varje rekommendation visar topp 3 motiveringar.
- Notiser triggas inom 10 sekunder efter villkor.
- Backtest-rapport för valfri lista med ≥5 års historik.

## Investeringsutbildning
- **Bolagsanalys:** affärsmodell, framtidsutsikter, konkurrens, ledning.
- **Nyckeltal:** P/E, Beta, utdelning.
- **Riskspridning & strategi:** definiera strategi, diversifiera, långsiktighet.
- **Kostnader:** courtage och valutaväxling.
