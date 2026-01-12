# CORS and PostgreSQL SSL Configuration Fix

## Summary

This document describes the security and compatibility improvements made to the HR Portal Azure deployment configuration.

## Changes Made

### 1. CORS Configuration Fix (`backend/app/main.py`)

**Problem:** The CORS middleware was using wildcard configuration (`allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]`), which poses a security risk by allowing any origin to access the API.

**Solution:**
- Changed `allow_origins` to use `settings.get_allowed_origins_list()` to respect the `ALLOWED_ORIGINS` environment variable
- Restricted `allow_methods` to only the necessary HTTP methods: `["GET", "POST", "PUT", "DELETE", "PATCH"]`
- Restricted `allow_headers` to only required headers: `["Content-Type", "Authorization"]`

**Configuration:**
Set the `ALLOWED_ORIGINS` environment variable in your `.env` file or Azure App Service configuration:
```bash
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://your-app.azurewebsites.net
```

### 2. PostgreSQL SSL Handling (`backend/app/database.py`)

**Problem:** The old implementation was stripping SSL parameters from the connection string without properly configuring asyncpg to use SSL, causing connection failures with Azure PostgreSQL which requires SSL.

**Solution:**
- Detect when SSL is required by checking for `sslmode=require` or `ssl=require` in the connection string
- Remove SSL parameters from the URL (asyncpg doesn't support them in the URL)
- Pass `connect_args={"ssl": "require"}` to `create_async_engine` when SSL is required

**How it works:**
```python
# Before: SSL parameters were stripped but not properly configured
# After: SSL is detected and properly configured
if ssl_required:
    engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        connect_args={"ssl": "require"}
    )
```

### 3. PostgreSQL SSL Handling for Alembic (`backend/alembic/env.py`)

**Problem:** Alembic migrations had the same SSL handling issue as the main database connection.

**Solution:**
- Applied the same SSL detection and configuration logic to Alembic's database connection
- Ensures database migrations work correctly with Azure PostgreSQL

**How it works:**
```python
# Prepare connect_args for SSL if required
connect_args = {}
if ssl_required:
    connect_args = {"ssl": "require"}

connectable = async_engine_from_config(
    configuration,
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
    connect_args=connect_args,
)
```

## Testing

### Automated Tests
A comprehensive test suite was created in `backend/tests/test_cors_and_ssl.py` that verifies:
- CORS configuration uses the correct origins, methods, and headers
- SSL detection logic works for various database URL formats
- URL cleaning properly removes SSL parameters
- All configuration files have the correct implementation

Run the tests:
```bash
cd backend
python3 tests/test_cors_and_ssl.py
```

### Verification Script
A manual verification script is available at `backend/verify_config.py` that:
- Shows the current CORS configuration from settings
- Tests SSL detection logic with various URL formats
- Provides clear output about what configurations will be used

Run the verification:
```bash
cd backend
python3 verify_config.py
```

## Deployment Checklist

Before deploying to Azure:

1. **Set ALLOWED_ORIGINS environment variable**
   ```bash
   ALLOWED_ORIGINS=https://your-frontend.com,https://your-api.azurewebsites.net
   ```

2. **Ensure DATABASE_URL includes SSL requirement for Azure PostgreSQL**
   ```bash
   DATABASE_URL=postgresql://user@host:5432/db?sslmode=require
   ```

3. **Verify changes locally** (optional)
   ```bash
   cd backend
   python3 tests/test_cors_and_ssl.py
   python3 verify_config.py
   ```

4. **Deploy to Azure**
   - The changes are already committed to the branch
   - Azure App Service will automatically use the new configuration
   - SSL will be automatically enabled for Azure PostgreSQL connections

## Security Improvements

1. **CORS Hardening**
   - No longer accepts requests from any origin
   - Only allows specified HTTP methods
   - Only allows required headers
   - Reduces attack surface for cross-origin attacks

2. **SSL/TLS Enforcement**
   - Properly configures SSL for Azure PostgreSQL
   - Ensures encrypted connections to the database
   - Complies with Azure PostgreSQL security requirements

## Compatibility

These changes are **backward compatible**:
- Local development: Works with or without SSL (based on database URL)
- Azure PostgreSQL: Automatically uses SSL when required
- CORS: Defaults to allowing all origins if `ALLOWED_ORIGINS` is not set (for backward compatibility during migration)

## Support

If you encounter issues:
1. Check that `ALLOWED_ORIGINS` includes all domains that need to access the API
2. Verify that Azure PostgreSQL connection string includes `?sslmode=require`
3. Run the verification script to diagnose configuration issues
4. Check application logs for connection errors

## Files Modified

- `backend/app/main.py` - CORS configuration
- `backend/app/database.py` - Database SSL handling
- `backend/alembic/env.py` - Alembic SSL handling
- `backend/tests/test_cors_and_ssl.py` - Test suite (new)
- `backend/verify_config.py` - Verification script (new)
