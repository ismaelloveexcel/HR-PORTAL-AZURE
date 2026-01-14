# Post-Deployment Health Check Guide

> 🏥 **Automated health monitoring for Azure deployments**

## Overview

After every successful deployment to Azure, an automated health check workflow runs to verify that:

- ✅ Backend API is responding correctly
- ✅ Frontend is accessible
- ✅ API documentation is available
- ✅ Response times are acceptable

If any checks fail, an issue is automatically created to alert you.

---

## Required Configuration

### GitHub Secrets

The health check requires two secrets to be configured:

| Secret Name     | Value                                        | Purpose                           |
| --------------- | -------------------------------------------- | --------------------------------- |
| `BACKEND_URL`   | `https://baynunahhrportal.azurewebsites.net` | URL for backend health checks     |
| `FRONTEND_URL`  | `https://baynunahhrportal.azurewebsites.net` | URL for frontend accessibility    |

**To add these secrets:**

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add both `BACKEND_URL` and `FRONTEND_URL` with the value `https://baynunahhrportal.azurewebsites.net`

> **Note:** Since this is a monolithic deployment (backend serves frontend), both URLs should be identical.

---

## What the Health Check Does

### Backend Health Check

**Endpoint:** `GET /health`

**Expected Response:**
```json
{
  "status": "ok"
}
```

**HTTP Status:** 200

**Note:** This endpoint is **publicly accessible** (no authentication required) - this is standard practice for monitoring and health checks.

### Frontend Health Check

**Endpoint:** `GET /` (root URL)

**Expected:** HTML page loads successfully

**HTTP Status:** 200

### Smoke Tests

Additional automated checks:

1. **API Documentation** - Verifies `/docs` endpoint is accessible
2. **OpenAPI Schema** - Verifies `/openapi.json` is available
3. **Response Time** - Measures endpoint performance (should be < 3 seconds)

---

## When Health Checks Run

The health check workflow is triggered automatically:

- ✅ After every successful **"Deploy to Azure"** workflow
- ✅ After every successful **"Deploy Local"** workflow
- ⏱️ Waits 30 seconds after deployment to allow services to stabilize

You can view health check results in the **Actions** tab under "Post-Deployment Health Check".

---

## Understanding Health Check Results

### ✅ Healthy Status

**What it means:**
- All automated checks passed
- Backend is responding correctly
- Frontend is accessible
- API documentation is available

**What to do:**
- Perform manual verification checklist (see issue/PR comment)
- If manual tests pass, deployment is successful!

### ❌ Unhealthy Status

**What it means:**
- One or more automated checks failed
- An issue will be automatically created with details

**Common causes:**

1. **Secrets not configured**
   - `BACKEND_URL` or `FRONTEND_URL` not set
   - **Fix:** Add secrets as described above

2. **Authentication issue** (Fixed in this PR)
   - `/health` endpoint required authentication
   - **Fix:** Already applied - endpoint is now public

3. **App not started yet**
   - Azure App Service is still starting up
   - **Fix:** Wait 2-3 minutes and re-run the health check workflow

4. **Actual deployment issue**
   - Configuration error, database unreachable, etc.
   - **Fix:** Check Azure App Service logs:
     ```bash
     az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR
     ```

### ⚠️ Needs Manual Verification

**What it means:**
- Automated checks passed, but some aspects require human verification
- Database connectivity can't be fully tested without credentials

**What to do:**
- Complete the manual verification checklist:
  - [ ] Can log in with credentials
  - [ ] Employee list loads correctly
  - [ ] Compliance features working (visa tracking, etc.)
  - [ ] Can create/edit records
  - [ ] Documents upload successfully

---

## Troubleshooting Health Check Failures

### Issue: "BACKEND_URL secret is not configured"

**Solution:**
```bash
# Add the secret via GitHub CLI
gh secret set BACKEND_URL -b"https://baynunahhrportal.azurewebsites.net"

# Or manually via GitHub web interface:
# Settings → Secrets and variables → Actions → New repository secret
```

### Issue: Health check reports "unhealthy" but manual test works

**Diagnosis:**
```bash
# Test the endpoint manually
curl https://baynunahhrportal.azurewebsites.net/health

# Expected output:
{"status":"ok"}
```

**If manual test works:**
- The issue may have been temporary (app still starting)
- Re-run the health check workflow:
  1. Go to Actions tab
  2. Find "Post-Deployment Health Check"
  3. Click "Re-run jobs"

**If manual test fails:**
- Check Azure App Service status in Azure Portal
- Review application logs
- Verify DATABASE_URL and AUTH_SECRET_KEY are set correctly

### Issue: "Connection refused" or "timeout"

**Possible causes:**
1. Azure App Service is not running
2. Deployment failed silently
3. Network/firewall restrictions

**Solution:**
```bash
# Check if app is running
az webapp show --name BaynunahHRPortal --resource-group BaynunahHR --query state

# Restart the app if needed
az webapp restart --name BaynunahHRPortal --resource-group BaynunahHR

# Check recent logs
az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR
```

### Issue: Performance check shows "slow" response times

**Acceptable ranges:**
- **Excellent:** < 1 second
- **Good:** 1-3 seconds
- **Slow:** 3-5 seconds
- **Unacceptable:** > 5 seconds

**Common causes:**
- Cold start (first request after deployment)
- Database query performance
- Server resource constraints

**Solutions:**
1. **For cold starts:** Normal behavior, will improve after app warms up
2. **For persistent slowness:** 
   - Review database queries
   - Check server CPU/memory usage in Azure Portal
   - Consider scaling up App Service plan

---

## Manual Verification Checklist

Even when automated checks pass, perform these manual tests:

### 1. Authentication & Login
- [ ] Can access the portal at https://baynunahhrportal.azurewebsites.net
- [ ] Can log in with admin credentials (BAYN00008 / DOB: 16051988)
- [ ] JWT token is issued correctly
- [ ] Can access protected endpoints

### 2. Employee Management
- [ ] Employee list loads
- [ ] Can view employee details
- [ ] Search functionality works
- [ ] Can create new employee record
- [ ] Can edit existing employee

### 3. Compliance Features (Critical for UAE)
- [ ] Visa expiry dates display correctly
- [ ] Emirates ID tracking works
- [ ] Contract end dates calculate properly
- [ ] Compliance alerts visible
- [ ] Notifications working

### 4. Document Management
- [ ] Can upload documents
- [ ] Documents display correctly
- [ ] Can download documents
- [ ] Document metadata accurate

### 5. Core Workflows
- [ ] Onboarding flow works
- [ ] Recruitment requests can be created
- [ ] Pass generation works
- [ ] Reports generate correctly

---

## Re-running Health Checks

If a health check failed due to temporary issues:

### Option 1: Via GitHub Actions UI

1. Go to **Actions** tab
2. Select **Post-Deployment Health Check** workflow
3. Find the failed run
4. Click **Re-run jobs**

### Option 2: Via GitHub CLI

```bash
# List recent workflow runs
gh run list --workflow=post-deployment-health.yml

# Re-run a specific run
gh run rerun <run-id>
```

### Option 3: Trigger via API

```bash
# Requires GITHUB_TOKEN with workflow permissions
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/ismaelloveexcel/HR-PORTAL-AZURE/actions/runs/<run-id>/rerun
```

---

## Disabling Health Checks

If you need to temporarily disable automated health checks:

1. Go to `.github/workflows/post-deployment-health.yml`
2. Comment out the workflow triggers:
   ```yaml
   # on:
   #   workflow_run:
   #     workflows: ["Deploy to Azure", "Deploy Local"]
   #     types:
   #       - completed
   ```
3. Commit and push the change

**⚠️ Not recommended:** Health checks catch deployment issues early!

---

## Architecture Notes

### Why is `/health` publicly accessible?

The basic health check endpoint (`/health`) does not require authentication for these reasons:

1. **Industry standard:** Load balancers, monitoring tools, and orchestrators need unauthenticated health checks
2. **Deployment validation:** Automated checks can't authenticate without credentials
3. **No sensitive data:** The endpoint only returns `{"status": "ok"}`
4. **Security:** Sensitive health endpoints (`/health/db`, `/health/reset-admin-password`) remain protected

### Monolithic vs Microservices

This application uses a **monolithic architecture**:

- Backend (FastAPI) serves both API and frontend static files
- Frontend (React) is built and copied to `backend/static/`
- Single Azure App Service hosts everything
- `BACKEND_URL` and `FRONTEND_URL` are identical

This simplifies deployment but means:
- Backend issues affect frontend accessibility
- Scaling requires scaling the entire app
- Health checks only need one URL

---

## Related Documentation

- [GitHub Deployment Setup](GITHUB_DEPLOYMENT_SETUP.md) - Complete deployment guide
- [Azure Deployment Reference](AZURE_DEPLOYMENT_REFERENCE_GUIDE.md) - Azure-specific details
- [Troubleshooting Guide](../README.md#troubleshooting) - General troubleshooting

---

## Questions?

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/ismaelloveexcel/HR-PORTAL-AZURE/issues) for similar problems
2. Review Azure App Service logs
3. Create a new issue with:
   - Health check workflow run URL
   - Screenshot of error
   - Steps to reproduce
   - Expected vs actual behavior

---

*Last updated: 2026-01-14*
*Related issue: #40 - Post-Deployment Health Check Failed*
