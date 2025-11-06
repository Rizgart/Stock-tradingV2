# Frontend (Desktop)

Desktop-klienten byggs med React + Tauri för att leverera en snabb och native-lik upplevelse.

## Tech stack
- React 18 med TypeScript
- Vite för bundling
- Tauri 2.0
- Redux Toolkit + RTK Query för state och data
- Mantine/Chakra UI för komponenter och tema
- i18next för sv/en-översättningar

## Initial struktur
```
frontend/desktop
├── src/
│   ├── app/            # App-shell, routing, state
│   ├── features/       # Domain-moduler (watchlist, portfolio, settings)
│   ├── widgets/        # Dashboard-kort, grafer, indikatorer
│   ├── shared/         # UI-komponenter, hooks, utils
│   └── assets/         # Ikoner, lokalisering, teman
├── public/
└── package.json
```

## Designprinciper
- Modulära features med slice-baserad struktur.
- Dark-mode och kontrastläge från start.
- Responsiva layouter med CSS grid/flex för framtida mobil.
- Tillgänglighet via aria-attribut och tangentbordsnavigering.

## Nästa steg
1. Initiera Tauri + React-projekt (`npm create tauri-app@latest`).
2. Sätt upp internationellisering och theming.
3. Implementera dashboard med realtidskort och rekommendationslista.
4. Koppla RTK Query mot backend-API:t.

> **Obs!** Plattformsspecifika ikoner ignoreras i repo:t. Generera egna lokalt via `npx @tauri-apps/cli icon <ikon.svg>` innan paketering.
