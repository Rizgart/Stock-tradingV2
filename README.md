# AktieTipset

AktieTipset är en desktop-applikation byggd med React och Tauri som hjälper användare att upptäcka och bevaka aktier. Projektet kombinerar en modulär Python-backend (FastAPI) med en analysmotor som räknar fram köp- och säljsignaler baserade på både tekniska och fundamentala indikatorer.

## Översikt

- **Desktop**: Tauri + React, målplattformar macOS (Intel/Apple Silicon) och Windows 10/11.
- **Backend**: FastAPI (Python) med mikrotjänst-arkitektur.
- **Analysmotor**: Python-baserad modul som nyttjar `pandas`, `numpy`, `scikit-learn` och `ta-lib`.
- **Data**: Integration mot Massive API som primär datakälla med stöd för fler källor.
- **Språkstöd**: Svenska och engelska.

## Mål för MVP

1. Realtidskurser och historik från Massive API.
2. Grundläggande tekniska indikatorer (MA, MACD, RSI) och rankingmodell.
3. Rekommendationer med förklaringar av topp 3 faktorer.
4. Watchlist, notiser och bevakning.
5. Import av API-nyckel och visning av data inom 1 minut.

Kompletta krav och arkitektur beskrivs i [`docs/product_spec.md`](docs/product_spec.md) och [`docs/architecture.md`](docs/architecture.md).

## Projektstruktur

```
.
├── backend/             # FastAPI-backend och tjänster
├── analysis_engine/     # Analys- och rankinglogik
├── data_integration/    # Adaptrar mot externa datakällor
├── frontend/            # Desktop-klient (React + Tauri)
├── docs/                # Krav, arkitektur och design
└── README.md
```

## Kom igång

### Förkrav

- Python 3.11+
- Node.js 18+
- Rust toolchain (för Tauri)

### Backend

```bash
cd backend/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Analysmotor (lokal utveckling)

```bash
cd analysis_engine
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

### Frontend (desktop)

```bash
cd frontend/desktop
npm install
npm run tauri dev
```

## Testning och kvalitet

- Minst 80 % testtäckning för kritisk logik i analysmotorn.
- E2E-flöden för import, ranking och alert-hantering.
- Backtesting över flera tidsperioder (6m–10y) med måtten CAGR, Sharpe, Max Drawdown och Win Rate.

## Juridisk disclaimer

> Appen ger informations- och utbildningssyfte, ej personlig finansiell rådgivning. Historisk avkastning garanterar ej framtida resultat.
