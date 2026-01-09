import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.routers import admin, attendance, auth, employees, health, onboarding, passes, renewals

configure_logging()
settings = get_settings()
logger = get_logger(__name__)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup
    logger.info("Application startup", extra={"env": settings.app_env})
    
    # Start attendance scheduler for background jobs
    try:
        from app.services.attendance_scheduler import start_attendance_scheduler
        start_attendance_scheduler()
        logger.info("Attendance scheduler started")
    except Exception as e:
        logger.warning(f"Could not start attendance scheduler: {e}")
    
    yield
    
    # Shutdown
    try:
        from app.services.attendance_scheduler import stop_attendance_scheduler
        stop_attendance_scheduler()
        logger.info("Attendance scheduler stopped")
    except Exception as e:
        logger.warning(f"Could not stop attendance scheduler: {e}")
    
    logger.info("Application shutdown")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
    
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(auth.router, prefix=settings.api_prefix)
    app.include_router(employees.router, prefix=settings.api_prefix)
    app.include_router(renewals.router, prefix=settings.api_prefix)
    app.include_router(passes.router, prefix=settings.api_prefix)
    app.include_router(onboarding.router, prefix=settings.api_prefix)
    app.include_router(attendance.router, prefix=settings.api_prefix)
    app.include_router(admin.router, prefix=settings.api_prefix)
    from app.routers import templates, audit_logs, notifications, activity_logs
    from app.routers import employee_compliance, employee_bank, employee_documents
    from app.routers import recruitment, interview, performance
    app.include_router(templates.router, prefix=settings.api_prefix)
    app.include_router(audit_logs.router, prefix=settings.api_prefix)
    app.include_router(notifications.router, prefix=settings.api_prefix)
    app.include_router(activity_logs.router, prefix=settings.api_prefix)
    app.include_router(employee_compliance.router)
    app.include_router(employee_bank.router)
    app.include_router(employee_documents.router)
    # Recruitment module - under admin section
    app.include_router(recruitment.router, prefix=settings.api_prefix)
    # Interview scheduling
    app.include_router(interview.router, prefix=settings.api_prefix)
    # Performance management
    app.include_router(performance.router, prefix=settings.api_prefix)
    # Employee of the Year nominations
    from app.routers import nominations
    app.include_router(nominations.router, prefix=settings.api_prefix)
    # Insurance Census management
    from app.routers import insurance_census
    app.include_router(insurance_census.router, prefix=settings.api_prefix)
    
    # Enhanced Attendance Module routers
    from app.routers import leave, public_holidays, timesheets, geofences
    app.include_router(leave.router, prefix=settings.api_prefix)
    app.include_router(public_holidays.router, prefix=settings.api_prefix)
    app.include_router(timesheets.router, prefix=settings.api_prefix)
    app.include_router(geofences.router, prefix=settings.api_prefix)

    @app.on_event("startup")
    async def on_startup():
        # Legacy startup hook (kept for compatibility, main logic in lifespan)
        pass

    @app.on_event("shutdown")
    async def on_shutdown():
        # Legacy shutdown hook (kept for compatibility, main logic in lifespan)
        pass

    # Serve static files in production (frontend build)
    static_dir = Path(__file__).parent.parent / "static"
    if static_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
        
        @app.get("/{full_path:path}")
        async def serve_spa(full_path: str):
            # Don't intercept API routes
            if full_path.startswith("api/"):
                return JSONResponse(status_code=404, content={"detail": "Not found"})
            # Serve index.html for all other routes (SPA routing)
            index_file = static_dir / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            return JSONResponse(status_code=404, content={"detail": "Frontend not built"})

    return app


app = create_app()
