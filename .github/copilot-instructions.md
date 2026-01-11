# Copilot Coding Agent Instructions for Secure Renewals HR Portal

## Project Overview

- **Full-stack HR portal** for employee contract renewals, onboarding, compliance, and recruitment.
- **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Alembic, asyncpg, modular routers (see `backend/app/routers/`).
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS (see `frontend/src/`).
- **Database:** PostgreSQL.
- **Authentication:** Employee ID + password (JWT); roles: admin, hr, viewer.

## Key Architectural Patterns

- **API-first:** All business logic via RESTful endpoints in `backend/app/routers/` and `backend/app/services/`.
- **Separation of concerns:**
  - `routers/`: API endpoints (per domain: employees, renewals, onboarding, passes, etc.)
  - `services/`: Business logic
  - `repositories/`: DB access
  - `schemas/`: Pydantic models for validation
- **Frontend:** Uses `/api` as base for all backend calls. State managed in `App.tsx`.
- **Onboarding:** Token-based public onboarding flow (see `/onboarding` endpoints).
- **Bulk operations:** CSV import/export for employees and updates (see `/employees/import`, `/employees/bulk-update`).
- **Compliance:** UAE-specific compliance fields and alerts (visa, Emirates ID, medical, ILOE, contract).

## Developer Workflows

- **Install dependencies:**
  - Backend: `cd backend && uv sync`
  - Frontend: `cd frontend && npm install`
- **Run locally:**
  - Backend: `cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
  - Frontend: `cd frontend && npm run dev`
- **Database migrations:**
  - Upgrade: `cd backend && uv run alembic upgrade head`
  - Create: `cd backend && uv run alembic revision --autogenerate -m "<msg>"`
- **Testing:** No formal test suite; use API docs at `/docs` and manual flows.
- **Deployment:** See `deploy_to_azure.sh`, Replit, Codespaces, or local scripts in `scripts/`.
- **Environment:** Use `.env` files for secrets/config (see `.env.example`).

## Project Conventions

- **Role-based access:** All protected endpoints require role via JWT; see `require_role` in backend.
- **Employee onboarding:**
  - HR/Admin generates invite link (`/onboarding/invite`)
  - Employee completes profile via tokenized link (no login required)
  - HR/Admin reviews and approves
- **CSV import:** Supports both Baynunah and simple formats; see docstrings in `/employees/import` endpoint.
- **Frontend routing:** SPA, all unknown routes serve `index.html` (see backend static file serving logic).
- **Feature toggles:** Admin-only, via `/admin/features` endpoints.

## AI Agent Usage

- **Specialized agents:**
  - HR Assistant: HR workflows, planning, module discovery
  - Portal Engineer: Full-stack implementation, migrations, debugging
  - Code Quality Monitor: Security, code quality, performance
- **Agent files:** See `.github/agents/` for agent-specific rules and quick reference.
- **Typical prompts:**
  - "Help me implement onboarding checklists"
  - "Create API endpoint for probation tracking"
  - "Scan for security vulnerabilities"

## Key Files & Directories

- `backend/app/routers/`: API endpoints (per domain)
- `backend/app/services/`: Business logic
- `backend/app/models/`: SQLAlchemy models
- `backend/app/schemas/`: Pydantic schemas
- `frontend/src/App.tsx`: Main React app, state, and API calls
- `.github/agents/`: Agent definitions and quick reference
- `docs/`: Full documentation and deployment guides

## Integration Points

- **Azure:** See `deploy_to_azure.sh` and `docs/AZURE_DEPLOYMENT_REFERENCE_GUIDE.md` for cloud deployment.
- **Replit:** See Replit section in `README.md` for secrets and domain setup.
- **Codespaces:** Supported for cloud dev; see `README.md`.

---

For more, see [README.md](../README.md), [docs/COPILOT_AGENTS.md](../docs/COPILOT_AGENTS.md), and `.github/agents/`.
