# Secure Renewals HR Portal

> 🏢 Internal application for securely managing employee contract renewals and onboarding checks.

[![License](https://img.shields.io/badge/license-ISC-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.3-blue.svg)](https://react.dev/)

---

## 📋 Table of Contents

- [Quick Start for HR Users](#-quick-start-for-hr-users)
- [Documentation](#-documentation)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Setup Guide](#-setup-guide)
- [Authentication](#-authentication)
- [Deployment](#-deployment)
- [Contributing](#-contributing)

---

## 🚀 Quick Start for HR Users

**New to the system?** Start here:

1. 📖 Read the [HR User Guide](docs/HR_USER_GUIDE.md) - Simple, step-by-step instructions
2. 🔑 Get your authentication token from IT
3. 🌐 Open the portal URL in your browser
4. ✅ Enter your token and start managing renewals!

**Need help?** Check the [Troubleshooting section](docs/HR_USER_GUIDE.md#troubleshooting) in the user guide.

---

## 📚 Documentation

| Document | Description | Audience |
|----------|-------------|----------|
| [HR User Guide](docs/HR_USER_GUIDE.md) | How to use the portal | HR Users |
| [System Health Check](docs/SYSTEM_HEALTH_CHECK.md) | Application assessment & roadmap | Admins/Developers |
| [Recommended Add-ons](docs/RECOMMENDED_ADDONS.md) | Integration options | Developers |

---

## ✨ Features

### Current Features
- ✅ **Contract Renewals** - Create, list, and track renewal requests
- ✅ **Role-Based Access** - Admin, HR, and Viewer roles
- ✅ **Audit Trail** - All actions logged for compliance
- ✅ **Simple Login** - Employee ID + password (DOB for first-time login)

### Coming Soon
- 🔜 **Onboarding Module** - New employee checklists
- 🔜 **External Users** - Contractor/vendor management
- 🔜 **Email Notifications** - Automated reminders
- 🔜 **CSV Import/Export** - Bulk operations

---

## 📁 Project Structure

```
Secure-Renewals-2/
├── backend/              # FastAPI Python API
│   ├── app/              # Application code
│   │   ├── routers/      # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Database access
│   │   ├── models/       # SQLAlchemy models
│   │   └── schemas/      # Pydantic schemas
│   └── alembic/          # Database migrations
├── frontend/             # React + TypeScript UI
│   └── src/              # React components
├── docs/                 # Documentation
│   ├── HR_USER_GUIDE.md
│   ├── SYSTEM_HEALTH_CHECK.md
│   └── RECOMMENDED_ADDONS.md
└── README.md
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy, Alembic |
| **Frontend** | React 18, TypeScript, Vite, TailwindCSS |
| **Database** | PostgreSQL (with asyncpg driver) |
| **Auth** | Employee ID + Password (JWT) |

---

## 📦 Setup Guide
### Prerequisites

- Python 3.11+

🔗 App available at: `http://localhost:5173`

---

## 🔐 Authentication

### Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access, auto-approve renewals, manage users |
| **HR** | Create renewals (need approval), view all employees |
| **Viewer** | Read-only access |

### Employee Login System

Employees log in using their **Employee ID** and a password:

1. **First-time Login:**
   - Enter your **Employee ID**
   - Enter your **Date of Birth** (DOB) as initial password
   - System prompts you to **create a new password**
   - Password must meet security requirements (min 8 characters, mixed case, number)

2. **Subsequent Logins:**
   - Enter your **Employee ID**
   - Enter your **password**

### Password Reset

If you forget your password:
1. Click "Forgot Password" on the login page
2. Enter your Employee ID
3. System sends a reset link (or HR can reset manually)

### Environment Variables

```env
# Authentication settings
AUTH_SECRET_KEY=<your-secret-key-for-jwt>
PASSWORD_MIN_LENGTH=8
SESSION_TIMEOUT_MINUTES=480
```

### Development Mode

For local testing:

```env
DEV_AUTH_BYPASS=true
DEV_USER_ID=EMP001
DEV_USER_ROLE=admin
```

---

## 🚀 Deployment

### Replit Deployment (Recommended)

The app is configured for **Replit** deployment under your company domain.

**Auto-configured features:**
- ✅ Frontend runs on port 5000 (external port 80)
- ✅ Backend runs on port 5001 (external port 3000)
- ✅ PostgreSQL available via Nix packages
- ✅ One-click run via Replit workflows

**Setup Steps:**

1. **Import to Replit**: Fork or import this repo to your Replit workspace
2. **Configure Secrets** (in Replit Secrets tab):
   ```
   DATABASE_URL=postgresql+asyncpg://...
   AUTH_ISSUER=https://login.microsoftonline.com/<tenant-id>/v2.0
   AUTH_AUDIENCE=api://secure-renewals
   AUTH_JWKS_URL=https://login.microsoftonline.com/<tenant-id>/discovery/v2.0/keys
   ALLOWED_ORIGINS=https://your-replit-app.your-company.com
   ```
3. **Set Custom Domain**: In Replit → Settings → Custom Domains, add your company domain
4. **Run**: Click the Run button - frontend and backend start automatically

**Replit-specific URLs:**
- Frontend: `https://your-app-name.your-company.com`
- Backend API: `https://your-app-name.your-company.com:3000/api`
- API Docs: `https://your-app-name.your-company.com:3000/docs`

### Environment Variables

**Backend Secrets (Replit Secrets or `.env`):**
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
ALLOWED_ORIGINS=https://your-app.your-company.com
AUTH_ISSUER=https://login.microsoftonline.com/<tenant>/v2.0
AUTH_AUDIENCE=api://secure-renewals
AUTH_JWKS_URL=https://login.microsoftonline.com/<tenant>/discovery/v2.0/keys
```

**Frontend (auto-configured in Replit):**
```env
VITE_API_BASE_URL=https://your-app.your-company.com:3000/api
```

### Deployment Checklist

- [ ] Import repo to Replit workspace
- [ ] Configure Replit Secrets with database and auth settings
- [ ] Set custom company domain in Replit settings
- [ ] Run database migrations (`cd backend && uv run alembic upgrade head`)
- [ ] Click Run to start the application
- [ ] Add admin user (first user with admin role)
- [ ] Share portal URL with HR team

---

## 🤝 Contributing

1. Check the [System Health Check](docs/SYSTEM_HEALTH_CHECK.md) for current priorities
2. Review [Recommended Add-ons](docs/RECOMMENDED_ADDONS.md) for enhancement ideas
3. Create an issue to discuss your proposal
4. Submit a pull request

---

## 📄 License

ISC License - See [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Secure Renewals HR Portal</strong><br>
  Built with ❤️ for HR teams
</p>
=======
## Tech Stack
- **Backend:** Python 3.11+, FastAPI, Uvicorn, Pydantic Settings, SQLAlchemy (async), Alembic
- **Frontend:** Vite, React, TypeScript, TailwindCSS

## Backend Setup
1. Navigate to `backend/`.
2. Create an `.env` file (see `.env.example`). Ensure `DATABASE_URL` points to your PostgreSQL instance (asyncpg driver).
3. Install dependencies with `uv sync` (or `pip install -r` from a generated requirements list if preferred).
4. Apply migrations: `uv run alembic upgrade head` (from the `backend` directory).
5. Run the API: `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

The API serves OpenAPI docs at `http://localhost:8000/docs`.

## Frontend Setup
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Create a `.env` file with `VITE_API_BASE_URL=http://localhost:8000/api`.
4. Start the dev server: `npm run dev` (defaults to `http://localhost:5173`).
5. Provide a role context (e.g., `admin`, `hr`, or `viewer`) in the UI header input so requests include the `X-Role` header expected by the API.

## Deployment Notes
- Configure HTTPS termination at your ingress or proxy layer.
- Set `ALLOWED_ORIGINS` in the backend `.env` to the deployed frontend URL (comma-separated for multiples).
- Run `uv run alembic upgrade head` after configuring your database credentials before starting the API in new environments.
- Run backend and frontend as separate services or containers; no Replit-specific files remain.
- Update `backend/uv.lock` via `uv lock` in a networked environment before production deployment.

## Authorization & Roles

- **Out of scope for this phase:** Authentication and identity are handled by upstream systems. This project does not issue, validate, or store tokens, and no login endpoints exist.
- **Role context:** An external caller injects role information. For local testing, supply one of `admin`, `hr`, or `viewer` via the `X-Role` header (exposed in the UI input).
- **Permissions:** `admin` can list and create; `hr` can create and list; `viewer` can list.

## Database & Audit
- PostgreSQL persistence using SQLAlchemy 2.0 async engine.
- Alembic migrations manage schema changes.
- Audit logging captures renewal creation/updates with snapshots for traceability.
>>>>>>> origin/codex/add-database-and-audit-layer-to-secure-renewals
