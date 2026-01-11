# HR Portal Deployment Guide (VS Code)

## PostgreSQL Setup via VS Code

### Step 1: Connect to PostgreSQL from VS Code

Your PostgreSQL server uses **Private Access (VNet)**, so use the VS Code extension:

1. **In Azure Portal:**
   - Go to `baynunahhrportal-server`
   - Click **"Connect from VS Code"**
   - Follow prompts to install PostgreSQL extension
2. **Server Details:**
   - Server: `baynunahhrportal-server.postgres.database.azure.com`
   - Admin user: `uutfqkhm`
   - Password: (retrieve from Azure Portal → Settings → Reset password if needed)
   - Port: `5432`
   - SSL: Required

### Step 2: Create Database

Once connected in VS Code PostgreSQL extension:

```sql
CREATE DATABASE hrportal;
```

Or use Azure Portal → Databases → Add database → Name: `hrportal`

### Step 3: Get Connection String

```
postgresql+asyncpg://uutfqkhm:<password>@baynunahhrportal-server.postgres.database.azure.com:5432/hrportal?ssl=require
```

**Note:** If using private link, your App Service needs to be in the same VNet or have VNet integration enabled.

---

## App Service Deployment

### Option A: Public PostgreSQL (Recommended)

Since your PostgreSQL uses private networking, you have 2 options:

1. **Enable public access** on PostgreSQL server:

   - Go to PostgreSQL server → Settings → Networking
   - Enable "Public access"
   - Add firewall rule for App Service outbound IPs
   - Add your local IP for management

2. **Keep private + Enable VNet Integration** on App Service:
   - App Service → Settings → Networking → VNet Integration
   - Connect to `BaynunahHRPortalVnet`

### Option B: Deploy to Azure Static Web Apps + Container App

For simpler networking without VNet complexity:

1. **Frontend:** Deploy React app to Azure Static Web Apps
2. **Backend:** Deploy FastAPI to Azure Container Apps (supports VNet integration easily)
3. **Database:** Keep PostgreSQL private or make public with firewall rules

---

## Quick Deployment Steps

### 1. Configure VNet Integration (Required for Private PostgreSQL)

Your PostgreSQL uses Private Access, so App Service needs VNet Integration:

```bash
chmod +x scripts/setup_vnet_integration.sh
bash scripts/setup_vnet_integration.sh
```

This creates an App Service subnet in your VNet and enables integration.

### 2. Create Database

```sql
CREATE DATABASE hrportal;
```

### 3. Update App Service Configuration

```bash
az webapp config appsettings set \
  --name BaynunahHRPortal \
  --resource-group BaynunahHR \
  --settings \
    DATABASE_URL="postgresql+asyncpg://uutfqkhm:<PASSWORD>@baynunahhrportal-server.postgres.database.azure.com:5432/hrportal?ssl=require" \
    AUTH_SECRET_KEY="$(openssl rand -hex 32)" \
    ALLOWED_ORIGINS="https://BaynunahHRPortal.azurewebsites.net" \
    APP_ENV="production"
```

### 4. Build and Deploy

```bash
# Build frontend
cd frontend
npm install
npm run build

# Copy to backend static folder
rm -rf ../backend/static
cp -r dist ../backend/static

# Deploy backend with frontend
cd ../backend
zip -r ../deploy.zip . -x "*.pyc" -x "__pycache__/*"
cd ..

az webapp deployment source config-zip \
  --resource-group BaynunahHR \
  --name BaynunahHRPortal \
  --src deploy.zip
```

### 5. Run Migrations

Option A - Using Azure CLI:

```bash
az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR
cd /home/site/wwwroot
python -m alembic upgrade head
```

Option B - Via Kudu Console:

- Go to: https://BaynunahHRPortal.scm.azurewebsites.net/
- Navigate to /home/site/wwwroot
- Run: `python -m alembic upgrade head`

---

## Troubleshooting

### Can't connect to PostgreSQL

- Check networking mode (public vs private)
- If private, ensure VNet integration is configured
- If public, add firewall rules for your IPs

### App Service won't start

- Check logs: `az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR`
- Verify all environment variables are set
- Check startup command in Configuration

### Database connection fails

- Verify connection string format
- Ensure `?ssl=require` is included
- Check admin credentials
- Test connection from VS Code first

---

## Post-Deployment

- **App URL:** https://BaynunahHRPortal.azurewebsites.net
- **API Docs:** https://BaynunahHRPortal.azurewebsites.net/docs
- **Logs:** Azure Portal → App Service → Log stream
