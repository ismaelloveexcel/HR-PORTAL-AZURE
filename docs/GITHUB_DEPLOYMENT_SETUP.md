# GitHub Actions Deployment Setup

> 🚀 **Deploy automatically to Azure on every push to `main` branch**

## Overview

This guide shows you how to set up automated deployment from GitHub to Azure using GitHub Actions. Every time you push code to the `main` branch, it will automatically:

1. Build the frontend (React + Vite)
2. Copy frontend to backend/static
3. Create deployment package
4. Deploy to Azure App Service
5. Configure environment variables

---

## Prerequisites

- Azure App Service created (BaynunahHRPortal)
- Azure PostgreSQL database configured
- GitHub repository with Actions enabled

---

## Step 1: Get Azure Service Principal

Create a service principal with contributor access to your App Service:

```bash
az ad sp create-for-rbac \
  --name "github-actions-hr-portal" \
  --role contributor \
  --scopes /subscriptions/<subscription-id>/resourceGroups/BaynunahHR \
  --sdk-auth
```

**Copy the entire JSON output** - you'll need it for GitHub secrets.

Output will look like:

```json
{
  "clientId": "xxxxx",
  "clientSecret": "xxxxx",
  "subscriptionId": "xxxxx",
  "tenantId": "xxxxx",
  ...
}
```

---

## Step 2: Add GitHub Secrets

Go to your GitHub repository:

1. Click **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add each of the following secrets:

### Required Secrets:

| Secret Name         | Value                                                                                                                            | Where to Get It                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `AZURE_CREDENTIALS` | JSON from Step 1                                                                                                                 | Service principal output         |
| `DATABASE_URL`      | `postgresql+asyncpg://uutfqjkrhm:eC71&&jm5#V7oGO#@baynunahhrportal-server.postgres.database.azure.com:5432/hrportal?ssl=require` | PostgreSQL connection string     |
| `AUTH_SECRET_KEY`   | Random 32-byte hex string                                                                                                        | Generate: `openssl rand -hex 32` |
| `OPENAI_API_KEY`    | `sk-proj-l4rHktOS7teKxUpq...`                                                                                                    | Your OpenAI API key              |
| `BACKEND_URL`       | `https://baynunahhrportal.azurewebsites.net`                                                                                     | Your Azure Web App URL           |
| `FRONTEND_URL`      | `https://baynunahhrportal.azurewebsites.net`                                                                                     | Same as BACKEND_URL (monolithic) |

> **Note:** `BACKEND_URL` and `FRONTEND_URL` are required for the automated post-deployment health checks. Since this is a monolithic deployment (backend serves frontend), both URLs should be the same.

---

## Step 3: Verify Workflow File

The workflow file is already configured at `.github/workflows/deploy.yml`. It includes:

✅ **Secrets validation** - Fails early if required secrets are missing  
✅ **Frontend build** with Vite  
✅ **Static asset verification** - Ensures frontend is included  
✅ **Backend packaging** with all dependencies  
✅ **Azure App Service deployment**  
✅ **Environment variable configuration** (DATABASE_URL, AUTH_SECRET_KEY)  
✅ **Automatic database migrations** - Runs `alembic upgrade head` post-deploy

No changes needed unless you want to customize!

---

## Step 4: Trigger Deployment

### Option A: Push to Main Branch

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### Option B: Manual Trigger

1. Go to GitHub → **Actions** tab
2. Select **Deploy to Azure** workflow
3. Click **Run workflow** → **Run workflow**

---

## Step 5: Monitor Deployment

1. Go to GitHub → **Actions** tab
2. Click on the running workflow
3. Watch real-time logs for each step:
   - ✅ Validate secrets
   - ✅ Build frontend
   - ✅ Verify static assets
   - ✅ Package backend
   - ✅ Deploy to Azure
   - ✅ Configure app settings
   - ✅ Run database migrations

Deployment typically takes **3-5 minutes**.

**Note:** The migration step may fail if the app is still starting up. If it fails, you can run migrations manually (see Troubleshooting).

---

## Step 6: Verify Deployment

Once complete, check:

1. **App URL:** https://baynunahhrportal.azurewebsites.net
2. **API Docs:** https://baynunahhrportal.azurewebsites.net/docs
3. **Health Check:** https://baynunahhrportal.azurewebsites.net/health

### Automated Health Checks

After each deployment, a **Post-Deployment Health Check** workflow automatically runs to verify:

- ✅ Backend API is responding (HTTP 200 from `/health`)
- ✅ Frontend is accessible (HTTP 200 from root URL)
- ✅ API documentation is available
- ⚠️ Database connectivity (requires manual verification)

**If health checks fail**, an issue will be automatically created with troubleshooting steps. Check the **Actions** tab for health check results.

> **Important:** Make sure `BACKEND_URL` and `FRONTEND_URL` secrets are configured (see Step 2) for automated health checks to work properly.

---

## Troubleshooting

### Post-Deployment Health Check Failed

- **Issue:** Automated health check reports backend or frontend as "unhealthy"
- **Fix:** 
  1. Verify `BACKEND_URL` and `FRONTEND_URL` secrets are set correctly:
     - Both should be `https://baynunahhrportal.azurewebsites.net`
     - Go to Settings → Secrets and variables → Actions
  2. Test manually by visiting https://baynunahhrportal.azurewebsites.net/health
     - Should return `{"status": "ok"}`
  3. If manual test works but automated check fails, verify GitHub Actions can reach the URL (check for IP restrictions)
  4. Check Azure App Service logs for startup errors:
     ```bash
     az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR
     ```

### Workflow Fails at "Validate required secrets"

- **Issue:** One or more required secrets (AZURE_CREDENTIALS, DATABASE_URL, AUTH_SECRET_KEY) are missing
- **Fix:** Add all required secrets in GitHub Settings → Secrets and variables → Actions

### Deployment Fails at "Login to Azure"

- **Issue:** AZURE_CREDENTIALS secret is invalid
- **Fix:** Verify secret matches service principal JSON exactly (including quotes)

### Deployment Succeeds but App Won't Start

- **Issue:** DATABASE_URL or AUTH_SECRET_KEY incorrect
- **Fix:** 
  1. Verify secrets are correct in GitHub Settings
  2. Check Azure Portal → App Service → Configuration to verify settings were applied
  3. Review app logs: `az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR`

### Frontend Not Loading

- **Issue:** Build output not in backend/static
- **Fix:** Check workflow logs for "Verify frontend build in backend/static" step. Should show index.html and assets directory.

### Database Migrations Failed

- **Issue:** Migration step timed out or couldn't connect
- **Fix:** Run migrations manually:
  ```bash
  az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR
  cd /home/site/wwwroot
  python -m alembic upgrade head
  ```

### Database Connection Error

- **Issue:** DATABASE_URL incorrect or database not accessible
- **Fix:** Verify VNet integration is enabled on App Service and connection string format is correct

---

## Environment-Specific Deployments

### Deploy to Staging

Create a separate workflow for staging environment:

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    # ... same as deploy.yml but use staging resources
    with:
      app-name: BaynunahHRPortal-Staging
```

Add staging-specific secrets:

- `STAGING_DATABASE_URL`
- `STAGING_AUTH_SECRET_KEY`

---

## Rollback

If a deployment causes issues:

### Option 1: Revert via Git

```bash
git revert HEAD
git push origin main
```

### Option 2: Redeploy Previous Version

1. GitHub → **Actions** → Select successful previous deployment
2. Click **Re-run jobs**

### Option 3: Manual Azure Rollback

```bash
az webapp deployment slot swap \
  --name BaynunahHRPortal \
  --resource-group BaynunahHR \
  --slot production \
  --target-slot staging
```

---

## Advanced Configuration

### Database Migrations

✅ **Already Configured!** The workflow automatically runs `alembic upgrade head` after deployment.

The migration step uses `continue-on-error: true` so it won't block the deployment if it fails. If migrations fail, you'll see clear instructions in the workflow logs for running them manually:

```bash
az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR
cd /home/site/wwwroot
python -m alembic upgrade head
```

### Deploy Notifications

Add Slack/Teams notifications:

```yaml
- name: Notify Deployment
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "✅ HR Portal deployed successfully!"
      }
```

---

## Cost Optimization

GitHub Actions minutes:

- **Free tier:** 2,000 minutes/month for public repos
- **Pro:** 3,000 minutes/month
- Each deployment uses ~5 minutes

**Tip:** Use `workflow_dispatch` for manual deployments to avoid unnecessary builds.

---

## Security Best Practices

✅ Never commit secrets to repository  
✅ Use service principal with minimal permissions  
✅ Rotate secrets regularly (every 90 days)  
✅ Enable GitHub secret scanning  
✅ Use environment protection rules for production

---

## Next Steps

1. ✅ Set up GitHub secrets
2. ✅ Push code to `main` branch
3. ✅ Watch deployment succeed
4. 📊 Monitor application in Azure Portal
5. 🔔 Set up deployment notifications (optional)

**Questions?** Check the [Azure Deployment Reference Guide](AZURE_DEPLOYMENT_REFERENCE_GUIDE.md)
