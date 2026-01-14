# Azure App Service Deployment Fix - Exit Code 3

## Problem Summary

The HR Portal was experiencing crash-loop failures on Azure App Service with:
- **Exit code 3** (process started but exited immediately)
- **Failed startup probes** (Azure couldn't reach the application)
- **Circular import** issues preventing proper module loading

## Root Causes Identified

### 1. Incorrect Startup Command
**Problem:** `azure_startup.sh` was using direct `uvicorn` instead of `gunicorn` with uvicorn workers.

**Why it matters:** 
- Azure Oryx build system expects Gunicorn for production Python apps
- Direct uvicorn doesn't integrate well with Azure's process management
- Port was hardcoded to 8000 instead of using Azure's `$PORT` environment variable

### 2. Circular Import in app.main
**Problem:** `app/routers/recruitment.py` imported `limiter` from `app.main`, while `app.main` imported all routers.

**Impact:**
- Created circular dependency: `main → routers → recruitment → main`
- Caused import errors and prevented app from starting
- Python would exit with code 3 when hitting the circular import

### 3. Over-complex Startup Script
**Problem:** Original script tried to:
- Create virtual environments
- Install dependencies
- Run database migrations
- Initialize database tables
- All before starting the app

**Impact:**
- Extended startup time beyond Azure's timeout
- Oryx already handles dependency installation
- Migrations should run via application lifecycle, not startup script

## Solutions Implemented

### Fix 1: Proper Gunicorn Startup Command

**File:** `backend/azure_startup.sh`

**Before:**
```bash
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**After:**
```bash
export PORT="${PORT:-8000}"
exec gunicorn app.main:app \
    --bind 0.0.0.0:$PORT \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
```

**Benefits:**
- ✅ Uses Azure's `$PORT` environment variable
- ✅ Gunicorn provides proper process management
- ✅ Uvicorn workers maintain ASGI compatibility
- ✅ Logs go to stdout/stderr for Azure monitoring
- ✅ 120-second timeout handles startup migrations

### Fix 2: Broke Circular Import

**Created:** `backend/app/core/rate_limit.py`

```python
"""Rate limiting configuration for the application."""
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a single limiter instance to be used across the application
# This avoids circular imports when routers need access to the limiter
limiter = Limiter(key_func=get_remote_address)
```

**Updated Files:**
1. `app/main.py` - Import limiter from `app.core.rate_limit` instead of creating it
2. `app/routers/recruitment.py` - Import limiter from `app.core.rate_limit` instead of `app.main`

**Benefits:**
- ✅ Eliminates circular dependency
- ✅ Single limiter instance shared across app
- ✅ Cleaner separation of concerns
- ✅ App can import without errors

### Fix 3: Simplified Startup Script

**Removed from startup script:**
- Virtual environment creation (Oryx handles this)
- Dependency installation (Oryx does this during deployment)
- Database table creation (handled by application startup migrations)

**Kept:**
- Proper port binding
- Gunicorn configuration
- Process execution

## Azure App Service Python Requirements

### What Azure Expects

1. **Gunicorn with Uvicorn Workers**
   ```bash
   gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker
   ```

2. **Bind to $PORT Environment Variable**
   ```bash
   --bind 0.0.0.0:$PORT
   ```

3. **Single ASGI Entrypoint**
   - Must have `app = create_app()` at module level in `app/main.py`
   - Gunicorn calls `app.main:app` directly

4. **Requirements in requirements.txt**
   ```
   gunicorn>=22.0.0
   uvicorn[standard]>=0.32.0
   ```

5. **Startup Command in Azure Configuration**
   ```bash
   az webapp config set --startup-file "bash azure_startup.sh"
   ```

## Testing the Fix

### 1. Local Testing

```bash
cd backend

# Test import (should not error)
python -c "from app.main import app; print('✅ Import successful')"

# Test with gunicorn locally
export PORT=8000
export DATABASE_URL="your-connection-string"
export AUTH_SECRET_KEY="your-secret-key"

gunicorn app.main:app \
    --bind 0.0.0.0:8000 \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 120 \
    --log-level debug

# Should start successfully and respond on http://localhost:8000
curl http://localhost:8000/health
# Expected: {"status":"ok"}
```

### 2. Azure Deployment Testing

After deploying:

```bash
# Check logs
az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR

# Expected to see:
# - "Starting Gunicorn with Uvicorn workers..."
# - Gunicorn startup messages
# - Application startup logs
# - No exit code 3 errors
# - No circular import errors

# Test health endpoint
curl https://baynunahhrportal.azurewebsites.net/health
# Expected: {"status":"ok"}

# Check app status
az webapp show \
    --name BaynunahHRPortal \
    --resource-group BaynunahHR \
    --query state

# Expected: "Running"
```

### 3. Verify No Crash Loop

```bash
# Monitor for 5 minutes to ensure stability
az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR

# Should NOT see:
# - Container crashed
# - Exit code 3
# - Startup probe failed
# - Continuous restart messages
```

## Common Azure App Service Issues

### Issue: "Container didn't respond to HTTP pings on port 8000"

**Cause:** App not binding to the correct port

**Fix:** Ensure `$PORT` environment variable is used:
```bash
export PORT="${PORT:-8000}"
gunicorn app.main:app --bind 0.0.0.0:$PORT
```

### Issue: "Site Has Not Loaded"

**Cause:** Startup taking too long or app crashing immediately

**Fix:** 
- Check `az webapp log tail` for errors
- Increase gunicorn timeout: `--timeout 120`
- Ensure no circular imports

### Issue: ModuleNotFoundError during import

**Cause:** Circular import or missing dependency

**Fix:**
- Check import chain for cycles
- Verify all dependencies in requirements.txt
- Test locally: `python -c "from app.main import app"`

### Issue: Exit Code 3

**Cause:** Process started but exited immediately, usually import error

**Fix:**
- Check for circular imports
- Ensure single app instance at module level
- Verify database connection string format

## Architecture Notes

### Gunicorn vs Uvicorn

**Uvicorn (ASGI server):**
- Fast ASGI implementation
- Single process
- Good for development
- No process management

**Gunicorn with Uvicorn workers:**
- Production-grade process manager
- Multiple workers
- Automatic restart on failure
- Graceful shutdown
- Better for Azure App Service

### Azure Oryx Build Process

1. **Build Phase** (during deployment):
   - Detects Python version from runtime.txt or requirements.txt
   - Creates virtual environment (antenv)
   - Installs dependencies from requirements.txt
   - Sets up environment

2. **Runtime Phase** (when app starts):
   - Runs startup command (azure_startup.sh)
   - Expects process to bind to $PORT
   - Sends HTTP probes to verify startup
   - Monitors process health

### Single vs Multiple Workers

For Azure B1 tier (1 vCPU, 1.75 GB RAM):
```bash
--workers 1  # Recommended
```

For higher tiers:
```bash
--workers $((2 * $(nproc) + 1))  # Formula: (2 × cores) + 1
```

## Deployment Checklist

Before deploying to Azure:

- [ ] `requirements.txt` includes gunicorn and uvicorn
- [ ] `azure_startup.sh` is executable (`chmod +x`)
- [ ] Startup command uses `$PORT` environment variable
- [ ] No circular imports in app code
- [ ] Single `app = create_app()` at module level
- [ ] Database migrations don't block startup (wrapped in try-except)
- [ ] Environment variables set in Azure App Settings:
  - `DATABASE_URL`
  - `AUTH_SECRET_KEY`
  - `ALLOWED_ORIGINS`
  - `APP_ENV=production`

## Rollback Plan

If issues persist after deploying these changes:

```bash
# Option 1: Redeploy previous working version
az webapp deployment slot swap \
    --name BaynunahHRPortal \
    --resource-group BaynunahHR \
    --slot staging

# Option 2: Use emergency test startup command
az webapp config set \
    --name BaynunahHRPortal \
    --resource-group BaynunahHR \
    --startup-file "gunicorn app.main:app --bind 0.0.0.0:\$PORT --worker-class uvicorn.workers.UvicornWorker"

# Option 3: SSH into container for debugging
az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR
cd /home/site/wwwroot
python -c "from app.main import app"  # Test import
```

## Additional Resources

- [Azure App Service Python Docs](https://learn.microsoft.com/en-us/azure/app-service/configure-language-python)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/settings.html)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/server-workers/)
- [Oryx Build System](https://github.com/microsoft/Oryx)

---

**Resolution Date:** 2026-01-14  
**Related Issue:** #40 - Post-Deployment Health Check Failed  
**Impact:** Fixes Azure App Service crash-loop, enables proper startup
