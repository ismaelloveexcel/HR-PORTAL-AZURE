# Copilot Coding Agent Instructions for Secure Renewals HR Portal

## Project Overview

**Full-stack HR portal** for employee contract renewals, onboarding, compliance, and recruitment targeting UAE-based startups with solo HR operations.

### Tech Stack at a Glance

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy (async), Alembic, asyncpg
- **Frontend:** React 18, TypeScript, Vite, TailwindCSS, single `App.tsx` monolith (5632 lines)
- **Database:** PostgreSQL (production) or SQLite (local development) with async support via `AsyncSessionLocal`
- **Auth:** Employee ID + password (JWT). Initial password = DOB in DDMMYYYY format. Roles: admin, hr, viewer
- **Package Management:** `uv` for Python, `npm` for JavaScript
- **Testing:** Manual testing via Swagger UI (`/docs`), no automated test suite currently

### Key Directories

```
HR-PORTAL-AZURE/
├── backend/app/
│   ├── routers/       # API endpoints (HTTP handlers)
│   ├── services/      # Business logic layer
│   ├── repositories/  # Database access layer
│   ├── models/        # SQLAlchemy ORM models
│   ├── schemas/       # Pydantic validation schemas
│   └── core/          # Config, security, utilities
├── frontend/src/
│   ├── App.tsx        # Main monolithic component (5632 lines)
│   └── components/    # Reusable UI components
├── docs/              # Comprehensive documentation
└── .github/
    ├── agents/        # Custom Copilot agents
    └── workflows/     # CI/CD automation
```

## Architecture Patterns

### Backend: 3-Layer Separation of Concerns
All features follow this pattern (see `backend/app/routers/employees.py` as canonical example):

1. **Router** (`routers/`) - FastAPI endpoints, auth via `require_role(["admin", "hr"])`, request/response handling
2. **Service** (`services/`) - Business logic, validation, orchestration
3. **Repository** (`repositories/`) - Database access using SQLAlchemy async queries

**Critical:** Never put business logic in routers or DB queries in services. Always use the repository layer for data access.

### Database & Migrations

- **Async-only:** All DB ops use `AsyncSession`, not sync Session
- **URL transformation:** Connection strings auto-convert `postgres://` → `postgresql+asyncpg://` (see `backend/app/database.py`)
- **Startup migrations:** `backend/app/startup_migrations.py` runs on app start for data consistency (employee normalization, admin seeding, etc.)
- **Migration commands:**
  ```bash
  cd backend
  uv run alembic upgrade head                  # Apply migrations
  uv run alembic revision --autogenerate -m "" # Generate new migration
  ```

### Frontend: Monolithic State Management

- **Single file:** `frontend/src/App.tsx` (5632 lines) manages all state and API calls
- **API base:** All backend calls use `/api` prefix (e.g., `fetch('/api/employees')`)
- **State:** Global state in `App.tsx`, passed down as props. No Redux/Context.
- **Routing:** Client-side in React; backend serves `index.html` for all non-API paths

## Developer Workflows

### Local Development

```bash
# Backend (port 8000)
cd backend && uv sync && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (port 5173)
cd frontend && npm install && npm run dev

# API docs: http://localhost:8000/docs
```

### VS Code Tasks (Pre-configured)

Use `Ctrl+Shift+B` → "Start Full Application" to run backend + frontend in parallel. See `.vscode/tasks.json`.

### Database Setup

```bash
cd backend
cp .env.example .env  # Edit DATABASE_URL
uv run alembic upgrade head
```

**No test suite:** Use `/docs` (Swagger UI) for manual testing. Production validates via startup migrations.

### Code Quality & Validation

When making changes, always:
1. **Backend:** Run `python -m py_compile backend/app/**/*.py` to check syntax
2. **Frontend:** Run `npm run lint` in frontend directory to check TypeScript
3. **Test manually:** Use Swagger UI at `http://localhost:8000/docs` to test API endpoints
4. **Check migrations:** After model changes, generate migration with `uv run alembic revision --autogenerate -m "description"`
5. **Verify startup:** Ensure `backend/app/startup_migrations.py` handles data consistency

## Critical Project Conventions

### Authentication Flow

1. **First login:** Employee uses Employee ID + DOB (DDMMYYYY) → forced password change
2. **Subsequent:** Employee ID + new password
3. **JWT:** Stored in `Authorization: Bearer <token>` header; validated via `require_role()` dependency

**Example:** See `backend/app/core/security.py:require_role()` for token validation logic.

### Employee Onboarding (Token-Based Public Flow)

Different from auth! Allows new employees to complete profile before activation:

1. HR/Admin: POST `/api/onboarding/invite` → generates token link
2. Employee: GET `/api/onboarding/validate/{token}` (no auth required)
3. Employee: POST `/api/onboarding/submit` (token in body)
4. HR/Admin: Reviews and approves in admin panel

**Key:** These endpoints have no `require_role()` dependency; token validates access.

### CSV Import Patterns

Employee import (`POST /api/employees/import`) supports **two formats**:

1. **Baynunah format** (auto-detected): Columns like "Employee No", "Employee Name", "Job Title"
2. **Simple format**: Headers `employee_id,name,email,department,date_of_birth,role`

**Critical:** Date parsing handles both `15061990` and `"March 11, 1979"` formats. See `backend/app/services/employees.py:import_from_csv()`.

### UAE Compliance Fields

All employees have compliance tracking fields (see `backend/app/models/employee_compliance.py`):

- Visa (number, issue/expiry dates)
- Emirates ID (number, expiry)
- Medical fitness (date, expiry)
- ILOE (status, expiry)
- Contract (type, start/end dates)

**Feature:** `/api/employees/compliance/alerts?days=60` returns expiring documents.

### Feature Toggles

Admin-only feature flags stored in `system_settings` table:

- GET `/api/admin/features` - List all toggles
- POST `/api/admin/features` - Enable/disable features

**Used for:** Rolling out new modules without code deployment.

## Integration Points

### Static File Serving (Production)

Backend serves frontend build from `backend/static/` or `frontend/dist/` (checks both). See `backend/app/main.py:100-115` for fallback logic.

**SPA routing:** All non-`/api` paths serve `index.html` for client-side routing.

### Deployment Options

- **Local:** `scripts/start-portal.sh` (auto-start available via `scripts/setup-autostart-macos.sh`)
- **Azure:** `deploy_to_azure.sh` + GitHub Actions workflows (see `docs/AZURE_DEPLOYMENT_REFERENCE_GUIDE.md`)
- **Replit:** Pre-configured in `.replit` with custom domain support
- **Codespaces:** Auto-configured dev container for cloud development

### Environment Variables

Required in `backend/.env`:

```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
AUTH_SECRET_KEY=<random-secret-for-jwt>
ALLOWED_ORIGINS=http://localhost:5173,https://your-domain.com
```

Optional: SMTP settings for email notifications (see `backend/app/core/config.py`).

## Common Implementation Patterns

### Adding a New Feature Module

1. **Model:** Create SQLAlchemy model in `backend/app/models/your_feature.py`
2. **Schema:** Pydantic models in `backend/app/schemas/your_feature.py` with validators
3. **Repository:** DB queries in `backend/app/repositories/your_feature.py`
4. **Service:** Business logic in `backend/app/services/your_feature.py`
5. **Router:** API endpoints in `backend/app/routers/your_feature.py` with `require_role()`
6. **Register:** Import in `backend/app/main.py` and `app.include_router(your_feature.router)`
7. **Migration:** Generate with `uv run alembic revision --autogenerate`
8. **Frontend:** Add component in `frontend/src/components/YourFeature.tsx`, integrate in `App.tsx`

**Example:** See `backend/app/routers/passes.py` for complete pattern (43-line router with 5 endpoints).

### Pydantic Validation + Sanitization

Always use `sanitize_text()` for user input (HTML escape):

```python
from app.core.security import sanitize_text
from pydantic import field_validator

@field_validator("name")
@classmethod
def sanitize_name(cls, value: str) -> str:
    return sanitize_text(value)
```

### Async Repository Pattern

```python
# Repository
async def list_all(self, session: AsyncSession) -> Sequence[Employee]:
    result = await session.execute(select(Employee).order_by(Employee.name))
    return result.scalars().all()

# Service
async def list_employees(self, session: AsyncSession) -> List[EmployeeResponse]:
    repo = EmployeeRepository()
    employees = await repo.list_all(session)
    return [EmployeeResponse.model_validate(e) for e in employees]
```

## AI Agent Ecosystem

This project has specialized agents for different tasks:

- **HR Assistant** (`.github/agents/hr-assistant.md`) - HR workflows, planning, module discovery
- **Portal Engineer** (`.github/agents/portal-engineer.md`) - Full-stack implementation, debugging
- **Code Quality Monitor** (`.github/agents/code-quality-monitor.md`) - Security scans, performance checks
- **Azure Deployment Specialist** (`.github/agents/azure-deployment-specialist.md`) - Azure deployment, troubleshooting

**Usage:** Reference agent files for specialized tasks. Example: "Use Portal Engineer pattern to add probation tracking."

## Security Best Practices

### Input Validation & Sanitization

**Always sanitize user input** to prevent XSS and injection attacks:

```python
from app.core.security import sanitize_text
from pydantic import field_validator, validator

class EmployeeCreate(BaseModel):
    name: str
    
    @field_validator("name")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        return sanitize_text(value)  # HTML escapes dangerous characters
```

### SQL Injection Prevention

**Never use string concatenation** for queries. Always use SQLAlchemy ORM or parameterized queries:

```python
# ❌ WRONG - SQL Injection vulnerability
query = f"SELECT * FROM employees WHERE name = '{name}'"

# ✅ CORRECT - Use SQLAlchemy
result = await session.execute(
    select(Employee).where(Employee.name == name)
)
```

### Authentication & Authorization

- **Check roles:** Use `require_role()` dependency for all protected endpoints
- **Verify JWT:** Token validation happens automatically via FastAPI dependencies
- **Password security:** Initial password is DOB, must be changed on first login
- **Session management:** JWT tokens expire based on `SESSION_TIMEOUT_MINUTES` config

```python
from app.core.security import require_role

@router.get("/employees")
async def list_employees(
    current_user: dict = Depends(require_role(["admin", "hr"])),
    db: AsyncSession = Depends(get_db)
):
    # Only admin and hr roles can access this endpoint
    pass
```

### Environment Variables & Secrets

**Never commit secrets** to the repository:
- ✅ Use `.env` file for local development (gitignored)
- ✅ Use Azure App Settings for production secrets
- ✅ Reference secrets via `os.getenv()` or Pydantic settings
- ❌ Never hardcode API keys, passwords, or connection strings

## Common Pitfalls & Troubleshooting

### Backend Issues

**Problem:** Async/sync mismatch errors
```python
# ❌ WRONG - Calling sync function in async context
def get_employees(db: Session):  # Sync session
    return db.query(Employee).all()

# ✅ CORRECT - Use async throughout
async def get_employees(db: AsyncSession):
    result = await db.execute(select(Employee))
    return result.scalars().all()
```

**Problem:** Database connection errors
- Check `DATABASE_URL` format: must be `postgresql+asyncpg://` for async or `sqlite:///` for SQLite
- For SQLite: Path must be relative to backend directory or absolute
- For PostgreSQL: Ensure database exists and credentials are correct

**Problem:** Migration conflicts
```bash
# Check migration history
uv run alembic history

# Merge conflicting heads
uv run alembic merge heads -m "Merge migrations"

# Apply migrations
uv run alembic upgrade head
```

### Frontend Issues

**Problem:** CORS errors when calling API
- Ensure `ALLOWED_ORIGINS` in backend `.env` includes frontend URL
- Default: `http://localhost:5173` for dev, production domain for prod

**Problem:** API calls failing with 401 Unauthorized
- Check JWT token is included in Authorization header
- Token format: `Bearer <token>`
- Verify token hasn't expired

**Problem:** TypeScript errors after dependency update
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Common Development Mistakes

1. **Mixing sync and async:** All database operations must be async
2. **Missing role checks:** All protected endpoints need `require_role()` dependency
3. **No input sanitization:** Always use `sanitize_text()` for user inputs
4. **Hardcoded values:** Use environment variables for configuration
5. **Direct DB access in routers:** Always go through service → repository layers
6. **Missing error handling:** Wrap async operations in try/except blocks

## Key Files Reference

- `backend/app/main.py` - App factory, router registration, static serving, startup migrations
- `backend/app/core/security.py` - JWT validation, role checking, input sanitization
- `backend/app/database.py` - Async SQLAlchemy setup, session factory
- `backend/app/startup_migrations.py` - Data consistency fixes on app start
- `frontend/src/App.tsx` - All frontend state, components, API calls (5632 lines)
- `docs/COPILOT_AGENTS.md` - Complete agent documentation
- `docs/AZURE_DEPLOYMENT_REFERENCE_GUIDE.md` - Cloud deployment patterns

## Quick Reference: Adding a New Feature

Here's a complete example of adding a new feature following project conventions:

### Example: Adding Employee Notes Feature

**1. Create Model** (`backend/app/models/employee_note.py`):
```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class EmployeeNote(Base):
    __tablename__ = "employee_notes"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, ForeignKey("employees.employee_id"))
    note = Column(Text, nullable=False)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    employee = relationship("Employee", back_populates="notes")
```

**2. Create Schema** (`backend/app/schemas/employee_note.py`):
```python
from pydantic import BaseModel, field_validator
from datetime import datetime
from app.core.security import sanitize_text

class EmployeeNoteCreate(BaseModel):
    employee_id: str
    note: str
    
    @field_validator("note")
    @classmethod
    def sanitize_note(cls, value: str) -> str:
        return sanitize_text(value)

class EmployeeNoteResponse(BaseModel):
    id: int
    employee_id: str
    note: str
    created_by: str
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**3. Create Repository** (`backend/app/repositories/employee_note.py`):
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from app.models.employee_note import EmployeeNote

class EmployeeNoteRepository:
    async def create(self, db: AsyncSession, note_data: dict) -> EmployeeNote:
        note = EmployeeNote(**note_data)
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    
    async def list_by_employee(self, db: AsyncSession, employee_id: str) -> Sequence[EmployeeNote]:
        result = await db.execute(
            select(EmployeeNote)
            .where(EmployeeNote.employee_id == employee_id)
            .order_by(EmployeeNote.created_at.desc())
        )
        return result.scalars().all()
```

**4. Create Service** (`backend/app/services/employee_note.py`):
```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.employee_note import EmployeeNoteRepository
from app.schemas.employee_note import EmployeeNoteCreate, EmployeeNoteResponse
from typing import List

class EmployeeNoteService:
    def __init__(self):
        self.repo = EmployeeNoteRepository()
    
    async def create_note(
        self, 
        db: AsyncSession, 
        note_data: EmployeeNoteCreate,
        created_by: str
    ) -> EmployeeNoteResponse:
        data = note_data.model_dump()
        data["created_by"] = created_by
        note = await self.repo.create(db, data)
        return EmployeeNoteResponse.model_validate(note)
    
    async def get_employee_notes(
        self, 
        db: AsyncSession, 
        employee_id: str
    ) -> List[EmployeeNoteResponse]:
        notes = await self.repo.list_by_employee(db, employee_id)
        return [EmployeeNoteResponse.model_validate(note) for note in notes]
```

**5. Create Router** (`backend/app/routers/employee_notes.py`):
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.core.security import require_role
from app.services.employee_note import EmployeeNoteService
from app.schemas.employee_note import EmployeeNoteCreate, EmployeeNoteResponse

router = APIRouter(prefix="/employee-notes", tags=["Employee Notes"])
service = EmployeeNoteService()

@router.post("", response_model=EmployeeNoteResponse)
async def create_note(
    note: EmployeeNoteCreate,
    current_user: dict = Depends(require_role(["admin", "hr"])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new employee note."""
    return await service.create_note(db, note, current_user["employee_id"])

@router.get("/{employee_id}", response_model=List[EmployeeNoteResponse])
async def get_notes(
    employee_id: str,
    current_user: dict = Depends(require_role(["admin", "hr"])),
    db: AsyncSession = Depends(get_db)
):
    """Get all notes for an employee."""
    return await service.get_employee_notes(db, employee_id)
```

**6. Register Router** (in `backend/app/main.py`):
```python
from app.routers import employee_notes

app.include_router(employee_notes.router, prefix="/api")
```

**7. Generate Migration**:
```bash
cd backend
uv run alembic revision --autogenerate -m "Add employee notes table"
uv run alembic upgrade head
```

**8. Frontend Integration** (in `frontend/src/App.tsx`):
```typescript
// Add to API calls section
const fetchEmployeeNotes = async (employeeId: string) => {
  const response = await fetch(`/api/employee-notes/${employeeId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};

const createEmployeeNote = async (data: { employee_id: string; note: string }) => {
  const response = await fetch('/api/employee-notes', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data)
  });
  return response.json();
};
```

---

## Additional Resources

- **README.md** - Project overview, quick start, deployment options
- **CONTRIBUTING.md** - Detailed setup instructions, contribution guidelines
- **docs/** - Extensive documentation including:
  - `HR_USER_GUIDE.md` - End-user documentation
  - `COPILOT_AGENTS.md` - AI agent usage guide
  - `AZURE_DEPLOYMENT_REFERENCE_GUIDE.md` - Cloud deployment
  - `VSCODE_DEPLOYMENT_GUIDE.md` - IDE setup and workflows

---

**For full documentation:** See [README.md](../README.md) | [CONTRIBUTING.md](../CONTRIBUTING.md) | [docs/](../docs/)
