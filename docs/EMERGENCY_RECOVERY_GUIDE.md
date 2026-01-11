# Emergency Admin Recovery - Usage Guide

## Overview

This document describes the new emergency admin recovery features added to the HR Portal.

## Features Added

### 1. Enhanced Login Error Logging

**Location:** `backend/app/routers/auth.py`

**Changes:**
- Login errors now log the employee_id attempting to login
- Full traceback is logged for debugging
- In development mode, actual error is returned to client
- In production mode, generic error with support instructions

**Example log output:**
```
ERROR Login error for employee_id=BAYN00008: Database connection failed
ERROR Login error traceback: Traceback (most recent call last)...
```

### 2. Database Health Check Endpoint

**Endpoint:** `GET /api/health/db`

**Purpose:** Check database connectivity and admin account status

**Response (Success):**
```json
{
  "database": "connected",
  "employee_count": 42,
  "admin_exists": true,
  "admin_details": {
    "employee_id": "BAYN00008",
    "name": "Admin User",
    "role": "admin",
    "is_active": true
  }
}
```

**Response (Failure):**
```json
{
  "detail": "Database connection failed: connection refused"
}
```

**Usage:**
```bash
# Check database health
curl http://localhost:8000/api/health/db

# Or on production
curl https://your-domain.com/api/health/db
```

### 3. Admin Password Reset Endpoint

**Endpoint:** `POST /api/health/reset-admin-password`

**Purpose:** Emergency password reset for BAYN00008 admin account

**Authentication:** Requires `X-Admin-Secret` header matching `AUTH_SECRET_KEY`

**Response (Success):**
```json
{
  "success": true,
  "message": "Password reset for BAYN00008 - Admin User",
  "employee_id": "BAYN00008",
  "name": "Admin User",
  "role": "admin",
  "is_active": true
}
```

**Note:** In development mode, response includes `"default_password": "16051988"` for convenience. This is not included in production for security reasons. The password is always `16051988` (admin's date of birth).

**Response (Failure):**
```json
{
  "detail": "Invalid secret token"
}
```

**Usage:**
```bash
# Local development
curl -X POST http://localhost:8000/api/health/reset-admin-password \
  -H "X-Admin-Secret: dev-secret-key-change-in-production"

# Production (replace with your actual AUTH_SECRET_KEY)
curl -X POST https://your-domain.com/api/health/reset-admin-password \
  -H "X-Admin-Secret: your-actual-secret-key"
```

### 4. Enhanced Startup Migration Logging

**Location:** `backend/app/main.py`

**Changes:**
- Success message logged when migrations complete
- Full traceback logged on migration failure
- Environment-aware error handling
- Recovery instructions in logs for production

**Example log output (success):**
```
INFO Startup migrations completed successfully
```

**Example log output (failure):**
```
ERROR Startup migrations failed: relation "employees" does not exist
ERROR Startup migration traceback: Traceback (most recent call last)...
ERROR Startup migration failed in production - use /api/health/reset-admin-password to recover
```

## Use Cases

### Case 1: Admin Cannot Login

**Problem:** Admin user BAYN00008 cannot login (wrong password, account locked, etc.)

**Solution:**
1. Check database health:
   ```bash
   curl https://your-domain.com/api/health/db
   ```

2. Reset admin password:
   ```bash
   curl -X POST https://your-domain.com/api/health/reset-admin-password \
     -H "X-Admin-Secret: YOUR_SECRET_KEY"
   ```

3. Login with employee_id `BAYN00008` and password `16051988`

4. Change password after login

### Case 2: Startup Migration Failure

**Problem:** Application starts but migrations fail

**Symptoms:**
- Server logs show "Startup migrations failed"
- Login attempts fail
- Database might be corrupted

**Solution:**
1. Check server logs for detailed traceback
2. Check database connectivity:
   ```bash
   curl https://your-domain.com/api/health/db
   ```
3. If database is connected but admin is missing/corrupted:
   ```bash
   curl -X POST https://your-domain.com/api/health/reset-admin-password \
     -H "X-Admin-Secret: YOUR_SECRET_KEY"
   ```

### Case 3: Development Debugging

**Problem:** Login fails during development, need to see actual error

**Solution:**
1. Set `APP_ENV=development` in environment
2. Attempt login
3. Error response will contain actual error message:
   ```json
   {
     "detail": "Login error: User not found in database"
   }
   ```
4. Check logs for full traceback

## Security Considerations

### Secret Token Protection

The `X-Admin-Secret` header must match the `AUTH_SECRET_KEY` environment variable:

- ✅ **DO:** Store in environment variables or secure vault
- ✅ **DO:** Use different values for dev/staging/prod
- ✅ **DO:** Rotate regularly
- ❌ **DON'T:** Hardcode in scripts
- ❌ **DON'T:** Commit to version control
- ❌ **DON'T:** Share via insecure channels

### Endpoint Access Control

- `/api/health/db` - Public (but should be behind firewall in production)
- `/api/health/reset-admin-password` - Protected by secret token

### Logging

All password reset attempts are logged with:
- Timestamp
- Success/failure status
- Employee ID being reset
- Warning on unauthorized attempts

## Testing

Run the test suite:
```bash
cd backend
pytest tests/test_emergency_endpoints.py -v
```

Run manual verification:
```bash
cd backend
python tests/manual_verification.py
```

## Rollback

If these changes cause issues, revert with:
```bash
git revert <commit-hash>
```

The application will function without these endpoints, but emergency recovery will require direct database access.
