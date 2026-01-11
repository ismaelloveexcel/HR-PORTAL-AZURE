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

---

## Step 3: Verify Workflow File

The workflow file is already configured at `.github/workflows/deploy.yml`. It includes:

✅ Frontend build with Vite  
✅ Backend packaging  
✅ Azure App Service deployment  
✅ Environment variable configuration

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
   - ✅ Build frontend
   - ✅ Package backend
   - ✅ Deploy to Azure
   - ✅ Configure settings

Deployment typically takes **3-5 minutes**.

---

## Step 6: Verify Deployment

Once complete, check:

1. **App URL:** https://baynunahhrportal.azurewebsites.net
2. **API Docs:** https://baynunahhrportal.azurewebsites.net/docs
3. **Health Check:** https://baynunahhrportal.azurewebsites.net/health

---

## Troubleshooting

### Deployment Fails at "Login to Azure"

- **Issue:** AZURE_CREDENTIALS secret is missing or invalid
- **Fix:** Verify secret matches service principal JSON exactly (including quotes)

### Deployment Succeeds but App Won't Start

- **Issue:** DATABASE_URL or other secrets missing
- **Fix:** Check all required secrets are added in GitHub Settings

### Frontend Not Loading

- **Issue:** Build output not copied to backend/static
- **Fix:** Check workflow logs for "Copy frontend build to backend" step

### Database Connection Error

- **Issue:** DATABASE_URL incorrect or database not accessible
- **Fix:** Verify VNet integration is enabled on App Service

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

### Add Database Migrations

Update workflow to run migrations after deployment:

```yaml
- name: Run Database Migrations
  run: |
    az webapp ssh \
      --name BaynunahHRPortal \
      --resource-group BaynunahHR \
      --command "cd /home/site/wwwroot && python -m alembic upgrade head"
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
