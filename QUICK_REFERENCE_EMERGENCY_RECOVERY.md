# Quick Reference: Emergency Recovery Endpoints

## 🚨 Emergency Scenarios

### Scenario 1: Admin Cannot Login
```bash
# Step 1: Check if database is healthy
curl http://localhost:8000/api/health/db

# Step 2: Reset admin password (requires AUTH_SECRET_KEY)
curl -X POST http://localhost:8000/api/health/reset-admin-password \
  -H "X-Admin-Secret: YOUR_AUTH_SECRET_KEY"

# Step 3: Login with BAYN00008 / 16051988
# Step 4: Change password when prompted
```

### Scenario 2: Debugging Login Failures
```bash
# Development Mode (shows actual errors)
export APP_ENV=development

# Production Mode (generic errors, detailed logs)
export APP_ENV=production

# Check server logs for:
# - "Login error for employee_id=XXXXX"
# - Full traceback
# - Recovery instructions
```

### Scenario 3: Startup Migration Issues
Check logs for:
```
✅ SUCCESS: "Startup migrations completed successfully"
❌ FAILURE: "Startup migrations failed: <error>"
           "Startup migration traceback: <full trace>"
           "Use /api/health/reset-admin-password to recover"
```

## 📊 API Quick Reference

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/health/db` | GET | None | Check database health |
| `/api/health/reset-admin-password` | POST | X-Admin-Secret | Reset admin password |
| `/api/auth/login` | POST | None | Login (enhanced logging) |

## 🔐 Security Notes

1. **X-Admin-Secret** header must match `AUTH_SECRET_KEY` environment variable
2. Password only shown in response in **development mode**
3. All reset attempts are **logged** for security audit
4. Production errors are **generic** to prevent info leakage
5. Development errors show **actual details** for debugging

## 📝 Response Examples

### Health Check - Success
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

### Health Check - Failure
```json
{
  "detail": "Database connection failed: connection refused"
}
```

### Password Reset - Success (Development)
```json
{
  "success": true,
  "message": "Password reset for BAYN00008 - Admin User",
  "employee_id": "BAYN00008",
  "name": "Admin User",
  "role": "admin",
  "is_active": true,
  "default_password": "16051988"  // Only in dev mode
}
```

### Password Reset - Success (Production)
```json
{
  "success": true,
  "message": "Password reset for BAYN00008 - Admin User",
  "employee_id": "BAYN00008",
  "name": "Admin User",
  "role": "admin",
  "is_active": true
  // No password in response for security
}
```

### Password Reset - Invalid Token
```json
{
  "detail": "Invalid secret token"
}
```

## 🧪 Testing Commands

```bash
# Run automated tests
cd backend
pytest tests/test_emergency_endpoints.py -v

# Run manual verification
python tests/manual_verification.py

# Run demo (shows examples)
python tests/demo_emergency_recovery.py
```

## 📚 Documentation Files

- `README.md` - Emergency recovery section
- `docs/EMERGENCY_RECOVERY_GUIDE.md` - Comprehensive guide
- `IMPLEMENTATION_SUMMARY.md` - Complete implementation details
- `backend/tests/demo_emergency_recovery.py` - Interactive demo

## 🔍 Log Patterns to Watch For

### Success Patterns
```
INFO Startup migrations completed successfully
INFO Admin password reset successful for BAYN00008
```

### Failure Patterns
```
ERROR Login error for employee_id=BAYN00008: <error>
ERROR Login error traceback: <full trace>
ERROR Startup migrations failed: <error>
ERROR Startup migration traceback: <full trace>
WARNING Unauthorized admin password reset attempt
```

## 🎯 Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `AUTH_SECRET_KEY` | Yes | JWT signing + admin reset auth |
| `APP_ENV` | No | `development` or `production` (default) |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `ADMIN_EMPLOYEE_ID` | No | Override admin employee ID (default: BAYN00008) |

## ⚠️ Important Notes

1. **Default Password:** Always `16051988` (admin's DOB in DDMMYYYY format)
2. **First Login:** System will force password change
3. **Token Security:** Never commit `AUTH_SECRET_KEY` to version control
4. **Audit Trail:** All reset attempts are logged with timestamps
5. **Database Access:** Health check and reset work even if migrations failed

## 🔄 Recovery Flow

```
1. Problem Detected
   ↓
2. Check Health (/api/health/db)
   ↓
3. Reset Password (/api/health/reset-admin-password)
   ↓
4. Login (BAYN00008 / 16051988)
   ↓
5. Change Password
   ↓
6. Normal Operations Resumed
```

## 📞 Support

For detailed information:
- Run: `python backend/tests/demo_emergency_recovery.py`
- Read: `docs/EMERGENCY_RECOVERY_GUIDE.md`
- Check: Server logs for detailed error traces

---

**Last Updated:** 2026-01-11  
**Version:** 1.0  
**Status:** Production Ready ✅
