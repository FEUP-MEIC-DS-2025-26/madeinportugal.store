# Frontend (TypeScript) — src

This folder contains the frontend-only TypeScript application. Backend services are split into separate microservices and are not part of this repository.

Recommended layout:

- `src/components/` — Reusable UI components.
- `src/pages/` — Route-level pages (for SPA or framework-driven routing).
- `src/hooks/` — Reusable React hooks.
- `src/services/` — API client wrappers to call backend microservices.
- `src/types/` — TypeScript type definitions and domain models.
- `src/utils/` — Small utility functions.
- `src/assets/` — Images, icons, fonts.
- `src/styles/` — Global styles, CSS modules, theme files.

Place small README or index files inside folders to describe conventions.
