# Frontend (Desktop)

Desktop-klienten byggs med Electron (JavaScript/TypeScript + React) för att leverera en snabb och native-lik upplevelse.

## Tech stack
- Electron (main/preload) med TypeScript
- React 18 med TypeScript
- Vite för renderer-bundling
- Redux Toolkit + RTK Query för state och data
- Mantine/Chakra UI för komponenter och tema
- i18next för sv/en-översättningar

## Initial struktur
```
frontend/desktop
├── electron/        # Electron main/preload-processer
├── src/
│   ├── app/         # App-shell, routing, state
│   ├── features/    # Domain-moduler (watchlist, portfolio, settings)
│   ├── widgets/     # Dashboard-kort, grafer, indikatorer
│   ├── shared/      # UI-komponenter, hooks, utils
│   └── assets/      # Ikoner, lokalisering, teman
├── public/
└── package.json
```

## Designprinciper
- Modulära features med slice-baserad struktur.
- Dark-mode och kontrastläge från start.
- Responsiva layouter med CSS grid/flex för framtida mobil.
- Tillgänglighet via aria-attribut och tangentbordsnavigering.

## Nästa steg
1. Initiera Electron + React-projekt, t.ex. via `npx create-electron-app@latest` eller Vite-baserad mall (`npm create @quick-start/electron`).
2. Lägg till delade renderer-/main-skript i `package.json` (t.ex. `npm run electron-dev` som startar både Vite och Electron main-processen via `concurrently`).
3. Sätt upp internationellisering och theming.
4. Implementera dashboard med realtidskort och rekommendationslista.
5. Koppla RTK Query mot backend-API:t.

> **Obs!** Plattformsspecifika ikoner ignoreras i repo:t. Generera egna lokalt och konfigurera `electron-builder` innan paketering.
