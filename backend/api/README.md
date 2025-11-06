# Backend API

FastAPI-baserat API som exponerar data till desktopklienten och externa integrationer.

## Funktioner
- Autentisering och hantering av API-nycklar.
- Proxy mot analysmotorn för rekommendationer.
- Endpoints för portfölj, alerts och datahämtning (under utveckling).

## Utvecklingsmiljö
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testning
Komplettera med pytest och httpx testclient.
