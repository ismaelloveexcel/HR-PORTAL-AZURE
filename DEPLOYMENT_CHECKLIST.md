# Azure Deployment Checklist

## Pre-Deployment Steps

### 1. Verify PostgreSQL Server

Run: `bash scripts/verify_postgresql.sh`

**Required Actions:**

- [ ] Confirm server is online
- [ ] Add firewall rule for App Service or enable "Allow Azure services"
- [ ] Create database: `az postgres flexible-server db create --server-name baynunahHRPortal-server --resource-group BaynunahHR --database-name hrportal`
- [ ] Get admin credentials

### 2. Configure Backend Environment

Update these in Azure App Service settings:

```bash
DATABASE_URL=postgresql+asyncpg://admin_user:password@baynunahHRPortal-server.postgres.database.azure.com:5432/hrportal?ssl=require
AUTH_SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALLOWED_ORIGINS=https://BaynunahHRPortal.azurewebsites.net
APP_ENV=production
PASSWORD_MIN_LENGTH=8
SESSION_TIMEOUT_MINUTES=480
```

### 3. Deploy Application

Run: `bash scripts/deploy_to_azure_app_service.sh`

**Manual Steps After Deployment:**

1. SSH into App Service: `az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR`
2. Run migrations: `cd /home/site/wwwroot && python -m alembic upgrade head`
3. Create first admin user (via API or seed script)

## Post-Deployment Verification

- [ ] Visit: https://BaynunahHRPortal.azurewebsites.net
- [ ] Check API docs: https://BaynunahHRPortal.azurewebsites.net/docs
- [ ] Test login with admin credentials
- [ ] Verify database connection in logs

## Troubleshooting

**If app doesn't start:**

- Check App Service logs: `az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR`
- Verify all environment variables are set
- Check startup command in App Service Configuration

**If database connection fails:**

- Verify firewall rules allow App Service
- Check connection string format
- Ensure SSL is enabled: `?ssl=require`
