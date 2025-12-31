# Secure Renewals

Internal application for securely managing employee contract renewals and onboarding checks. The project is split into a FastAPI backend and a Vite + TypeScript + Tailwind frontend to keep responsibilities isolated and deployment-ready.

## Project Structure
- `backend/` – FastAPI service exposing renewal APIs and OpenAPI docs.
- `frontend/` – Vite + React client that consumes the API via a typed service layer.
- `.gitignore` – Repository hygiene rules.

## Tech Stack
- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic Settings
- **Frontend:** Vite, React, TypeScript, TailwindCSS

## Backend Setup
1. Navigate to `backend/`.
2. Create an `.env` file (see `.env.example`). Ensure `DATABASE_URL` points to your PostgreSQL instance (asyncpg driver) and configure `AUTH_ISSUER`, `AUTH_AUDIENCE`, and `AUTH_JWKS_URL` to match your IdP (Azure AD / Entra ID by default).
3. Install dependencies with `uv sync` (or `pip install -r` from a generated requirements list if preferred).
4. Apply migrations: `uv run alembic upgrade head` (from the `backend` directory).
5. Run the API: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

The API serves OpenAPI docs at `http://localhost:8000/docs` and requires a bearer token (`Authorization: Bearer <JWT>`) carrying one of the allowed roles (admin, hr, viewer).

## Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Create a `.env` file with `VITE_API_BASE_URL=http://localhost:8000/api`.
4. Start the dev server: `npm run dev` (defaults to `http://localhost:5173`).
5. Paste a valid bearer token into the header field in the UI before making API calls.

## Deployment Notes
- Configure HTTPS termination at your ingress or proxy layer.
- Set `ALLOWED_ORIGINS` in the backend `.env` to the deployed frontend URL (comma-separated for multiples).
- Run `uv run alembic upgrade head` after configuring your database credentials before starting the API in new environments.
- Run backend and frontend as separate services or containers; no Replit-specific files remain.
- Update `backend/uv.lock` via `uv lock` in a networked environment before production deployment.

## Authentication & Authorization

- **Primary flow:** API expects JWTs issued by your IdP (Azure AD / Entra ID). Tokens are validated for issuer, audience, signature (via JWKS), and expiry, and roles are mapped from common claims (`roles`, `groups`, `appRoles`).
- **Roles:** `admin` (full access), `hr` (create + list), `viewer` (list only). Authorization is enforced centrally via FastAPI dependencies.
- **Local development:** Set `DEV_AUTH_BYPASS=true` and provide `DEV_STATIC_TOKEN=<preissued JWT>` in `.env` to allow offline testing without calling the IdP. The token must still be supplied as a bearer token in requests.
- **Security notes:** Tokens are not logged or stored; unsigned/malformed/expired tokens are rejected with 401/403 responses.

### Azure AD / Entra ID integration (high-level)

1. Register an app in Entra ID for the Secure Renewals API.
2. Configure an Application ID URI (e.g., `api://secure-renewals`) and assign app roles that contain `admin`, `hr`, or `viewer` in their names.
3. Expose the JWKS endpoint via the OpenID configuration for your tenant and set `AUTH_ISSUER`, `AUTH_AUDIENCE`, and `AUTH_JWKS_URL` accordingly.
4. Issue tokens to users or service principals, then supply them as `Authorization: Bearer <token>` to the API.
