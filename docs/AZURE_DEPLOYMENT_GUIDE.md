# Azure Deployment Guide

> 🚀 Complete guide for deploying Secure Renewals HR Portal to Microsoft Azure without manual intervention.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Prerequisites](#-prerequisites)
- [Azure Architecture](#-azure-architecture)
- [Infrastructure Provisioning](#-infrastructure-provisioning)
- [GitHub Secrets Configuration](#-github-secrets-configuration)
- [OIDC Setup for Passwordless Deployment](#-oidc-setup-for-passwordless-deployment)
- [Deployment Workflow](#-deployment-workflow)
- [Post-Deployment](#-post-deployment)
- [Troubleshooting](#-troubleshooting)
- [Cost Estimation](#-cost-estimation)

---

## 🚀 Quick Start

**Deploy in 3 steps:**

1. **Provision Azure resources** (one-time setup)
   ```bash
   ./deploy_to_azure.sh
   ```

2. **Configure GitHub Secrets** (from provision output)
   - `AZURE_CLIENT_ID`
   - `AZURE_TENANT_ID`
   - `AZURE_SUBSCRIPTION_ID`
   - `AZURE_STATIC_WEB_APPS_API_TOKEN`
   - `DATABASE_URL`
   - `API_BASE_URL`

3. **Push to main branch** - Automatic deployment begins!
   ```bash
   git push origin main
   ```

---

## ✅ Prerequisites

### Azure Requirements
- [ ] Active Azure subscription
- [ ] Contributor or Owner role on the subscription
- [ ] Azure CLI installed (`az --version`)

### GitHub Requirements
- [ ] Repository admin access
- [ ] GitHub Actions enabled
- [ ] Branch protection configured (recommended)

### Local Development
- [ ] Python 3.11+
- [ ] Node.js 20+
- [ ] uv package manager

---

## 🏗️ Azure Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     Resource Group: secure-renewals-rg                  │
│                         Region: UAE North                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    ┌─────────────────────────────────────────────────────────────┐     │
│    │                      Traffic Flow                           │     │
│    │                                                             │     │
│    │   Users → Azure Static Web App (Frontend)                   │     │
│    │              ↓                                              │     │
│    │           API Calls                                         │     │
│    │              ↓                                              │     │
│    │   Azure App Service (Backend - FastAPI)                     │     │
│    │              ↓                                              │     │
│    │   Azure Database for PostgreSQL Flexible Server             │     │
│    │                                                             │     │
│    └─────────────────────────────────────────────────────────────┘     │
│                                                                         │
│    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐    │
│    │ Azure Key Vault │   │ App Insights    │   │ Managed Identity│    │
│    │ (Secrets)       │   │ (Monitoring)    │   │ (Auth)          │    │
│    └─────────────────┘   └─────────────────┘   └─────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Resource Summary

| Resource | Type | SKU/Tier | Purpose |
|----------|------|----------|---------|
| Resource Group | - | - | Container for all resources |
| App Service Plan | Linux | B1 (Staging) / P1V2 (Prod) | Hosts backend |
| Web App | Python 3.11 | - | FastAPI backend |
| Static Web App | - | Free | React frontend |
| PostgreSQL | Flexible Server | B1ms (Staging) / GP_Gen5_2 (Prod) | Database |
| Key Vault | Standard | - | Secrets storage |
| Application Insights | - | - | Monitoring |

---

## 🔧 Infrastructure Provisioning

### Option 1: Using the Provision Script

```bash
# Make the script executable
chmod +x deploy_to_azure.sh

# Run the script
./deploy_to_azure.sh
```

### Option 2: Manual Provisioning

#### Step 1: Login to Azure
```bash
az login
az account set --subscription "<your-subscription-id>"
```

#### Step 2: Create Resource Group
```bash
RESOURCE_GROUP="secure-renewals-rg"
LOCATION="uaenorth"

az group create --name $RESOURCE_GROUP --location $LOCATION
```

#### Step 3: Create App Service Plan and Web App
```bash
APP_SERVICE_PLAN="secure-renewals-plan"
WEBAPP_NAME="secure-renewals-api"

# Create App Service Plan
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON:3.11"

# Create staging slot
az webapp deployment slot create \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --slot staging
```

#### Step 4: Create PostgreSQL Database
```bash
POSTGRES_SERVER="secure-renewals-db"
POSTGRES_DB="secure_renewals"
POSTGRES_ADMIN="sradmin"
POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --admin-user $POSTGRES_ADMIN \
  --admin-password "$POSTGRES_PASSWORD" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $POSTGRES_SERVER \
  --database-name $POSTGRES_DB

echo "Database URL: postgresql+asyncpg://${POSTGRES_ADMIN}:${POSTGRES_PASSWORD}@${POSTGRES_SERVER}.postgres.database.azure.com:5432/${POSTGRES_DB}?sslmode=require"
```

#### Step 5: Create Static Web App
```bash
# Create Static Web App (via Azure Portal or CLI)
az staticwebapp create \
  --name "secure-renewals-frontend" \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Free

# Get the deployment token
az staticwebapp secrets list \
  --name "secure-renewals-frontend" \
  --query "properties.apiKey" -o tsv
```

#### Step 6: Configure Web App
```bash
# Set startup command
az webapp config set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app"

# Enable managed identity
az webapp identity assign \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP

# Set environment variables
az webapp config appsettings set \
  --name $WEBAPP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    DATABASE_URL="<your-database-url>" \
    AUTH_SECRET_KEY="<your-secret-key>" \
    ALLOWED_ORIGINS="https://secure-renewals-frontend.azurestaticapps.net"
```

---

## 🔐 GitHub Secrets Configuration

Navigate to: **Repository Settings → Secrets and variables → Actions**

### Required Secrets

| Secret Name | Description | How to Get |
|-------------|-------------|------------|
| `AZURE_CLIENT_ID` | Azure AD App Client ID | See OIDC Setup below |
| `AZURE_TENANT_ID` | Azure AD Tenant ID | Azure Portal → Azure Active Directory → Overview |
| `AZURE_SUBSCRIPTION_ID` | Azure Subscription ID | Azure Portal → Subscriptions |
| `AZURE_STATIC_WEB_APPS_API_TOKEN` | Static Web App deployment token | Azure Portal → Static Web App → Manage deployment token |
| `DATABASE_URL` | PostgreSQL connection string | From provisioning output |
| `API_BASE_URL` | Backend API URL | `https://<webapp-name>.azurewebsites.net/api` |

---

## 🔑 OIDC Setup for Passwordless Deployment

Using OpenID Connect (OIDC) eliminates the need for storing long-lived credentials.

### Step 1: Create App Registration

```bash
# Create App Registration
az ad app create --display-name "secure-renewals-github-actions"

# Get the App ID
APP_ID=$(az ad app list --display-name "secure-renewals-github-actions" --query "[0].appId" -o tsv)
echo "AZURE_CLIENT_ID: $APP_ID"

# Create Service Principal
az ad sp create --id $APP_ID

# Get Object ID for role assignment
OBJECT_ID=$(az ad sp show --id $APP_ID --query "id" -o tsv)
```

### Step 2: Assign Permissions

```bash
SUBSCRIPTION_ID=$(az account show --query "id" -o tsv)

# Assign Contributor role to resource group
az role assignment create \
  --role Contributor \
  --assignee-object-id $OBJECT_ID \
  --assignee-principal-type ServicePrincipal \
  --scope "/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/secure-renewals-rg"
```

### Step 3: Create Federated Credential

```bash
# Create federated credential for main branch
az ad app federated-credential create --id $APP_ID --parameters '{
  "name": "github-main-branch",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:ismaelloveexcel/Secure-Renewals-2:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'

# Create federated credential for pull requests (optional)
az ad app federated-credential create --id $APP_ID --parameters '{
  "name": "github-pull-requests",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:ismaelloveexcel/Secure-Renewals-2:pull_request",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

### Step 4: Get Tenant ID

```bash
TENANT_ID=$(az account show --query "tenantId" -o tsv)
echo "AZURE_TENANT_ID: $TENANT_ID"
```

---

## 🔄 Deployment Workflow

### Automatic Deployment (Recommended)

The workflow triggers automatically on:
- Push to `main` branch (changes to `backend/` or `frontend/`)
- Manual trigger via `workflow_dispatch`

### Manual Deployment

1. Go to **Actions** tab in GitHub
2. Select **Deploy to Azure** workflow
3. Click **Run workflow**
4. Choose what to deploy:
   - Deploy backend: ✅
   - Deploy frontend: ✅

### Deployment Process

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Push to   │────▶│  Build &    │────▶│ Deploy to   │────▶│   Health    │
│    main     │     │   Test      │     │  Staging    │     │   Check     │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                    │
                    ┌─────────────┐     ┌─────────────┐            │
                    │  Complete!  │◀────│   Swap to   │◀───────────┘
                    │             │     │ Production  │
                    └─────────────┘     └─────────────┘
```

---

## 🔍 Post-Deployment

### Verify Deployment

1. **Check Backend Health**
   ```bash
   curl https://secure-renewals-api.azurewebsites.net/api/health
   ```

2. **Check Frontend**
   - Open: `https://secure-renewals-frontend.azurestaticapps.net`

3. **Run Database Migrations**
   ```bash
   az webapp ssh --name secure-renewals-api --resource-group secure-renewals-rg
   # Inside the container:
   cd /home/site/wwwroot
   uv run alembic upgrade head
   ```

### Monitor Application

```bash
# Tail logs
az webapp log tail --name secure-renewals-api --resource-group secure-renewals-rg

# View Application Insights
az monitor app-insights component show --app secure-renewals-api --resource-group secure-renewals-rg
```

### Configure Custom Domain (Optional)

```bash
# Add custom domain
az webapp config hostname add \
  --webapp-name secure-renewals-api \
  --resource-group secure-renewals-rg \
  --hostname "api.yourdomain.com"

# Enable managed SSL certificate
az webapp config ssl create \
  --resource-group secure-renewals-rg \
  --name secure-renewals-api \
  --hostname "api.yourdomain.com"
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Deployment Fails - Permission Denied
```
Error: The client with object id does not have authorization
```

**Solution:**
- Verify the service principal has Contributor role
- Check federated credential configuration matches repository and branch
- Ensure secrets are correctly set in GitHub

#### 2. Health Check Fails
```
Error: Connection refused
```

**Solution:**
```bash
# Check app logs
az webapp log tail --name secure-renewals-api --resource-group secure-renewals-rg

# Verify startup command
az webapp config show --name secure-renewals-api --resource-group secure-renewals-rg --query "linuxFxVersion"

# Restart the app
az webapp restart --name secure-renewals-api --resource-group secure-renewals-rg
```

#### 3. Database Connection Error
```
Error: Connection to PostgreSQL failed
```

**Solution:**
- Verify DATABASE_URL format: `postgresql+asyncpg://user:pass@host:5432/db?sslmode=require`
- Check firewall rules allow App Service IP
- Verify SSL mode is enabled

#### 4. Static Web App Build Fails
```
Error: Failed to detect package manager
```

**Solution:**
- Ensure `package-lock.json` exists
- Verify `output_location` is set to `dist`
- Check Vite build completes locally: `npm run build`

### Useful Commands

```bash
# View deployment status
az webapp deployment list --name secure-renewals-api --resource-group secure-renewals-rg

# View app settings
az webapp config appsettings list --name secure-renewals-api --resource-group secure-renewals-rg

# SSH into container
az webapp ssh --name secure-renewals-api --resource-group secure-renewals-rg

# Swap slots manually
az webapp deployment slot swap \
  --name secure-renewals-api \
  --resource-group secure-renewals-rg \
  --slot staging \
  --target-slot production

# Rollback (swap back)
az webapp deployment slot swap \
  --name secure-renewals-api \
  --resource-group secure-renewals-rg \
  --slot production \
  --target-slot staging
```

---

## 💰 Cost Estimation

### Development/Staging Environment

| Resource | SKU | Monthly Cost (USD) |
|----------|-----|-------------------|
| App Service Plan | B1 | ~$13 |
| PostgreSQL Flexible | B1ms | ~$15 |
| Static Web App | Free | $0 |
| **Total** | | **~$28/month** |

### Production Environment

| Resource | SKU | Monthly Cost (USD) |
|----------|-----|-------------------|
| App Service Plan | P1V2 | ~$75 |
| PostgreSQL Flexible | GP_Gen5_2 | ~$100 |
| Static Web App | Standard | ~$9 |
| Key Vault | Standard | ~$1 |
| Application Insights | Basic | ~$5 |
| **Total** | | **~$190/month** |

> 💡 **Tip**: Use Azure Calculator for precise estimates: https://azure.microsoft.com/pricing/calculator/

---

## 📚 Related Documentation

- [Azure Deployer Agent](.github/agents/azure-deployer.md)
- [Portal Engineer Agent](.github/agents/portal-engineer.md)
- [README - Deployment Section](README.md#-deployment)
- [Azure App Service Documentation](https://docs.microsoft.com/azure/app-service/)
- [Azure Static Web Apps Documentation](https://docs.microsoft.com/azure/static-web-apps/)

---

<p align="center">
  <strong>Secure Renewals HR Portal - Azure Deployment</strong><br>
  Zero-touch deployment for enterprise-ready HR solutions
</p>
