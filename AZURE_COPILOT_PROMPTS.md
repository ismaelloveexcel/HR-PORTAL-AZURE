# Azure Copilot Prompts for Automated Deployment

Use these prompts with Azure Copilot to automate configuration tasks.

## Prompt 1: Get PostgreSQL Password

```
Reset the password for PostgreSQL flexible server 'baynunahhrportal-server' in resource group 'BaynunahHR' and show me the connection details. Admin username is 'uutfqkhm'.
```

## Prompt 2: Complete Deployment Setup (All-in-One)

```
For HR Portal deployment in resource group 'BaynunahHR':

1. Reset password for PostgreSQL server 'baynunahhrportal-server' (admin: uutfqkhm) and save it
2. Create database 'hrportal' if it doesn't exist
3. In VNet 'BaynunahHRPortalVnet', create subnet 'AppServiceSubnet' with address prefix 10.0.1.0/24, delegated to Microsoft.Web/serverFarms
4. Enable VNet integration on App Service 'BaynunahHRPortal' using the new subnet
5. Verify the configuration is complete

Provide the PostgreSQL password at the end so I can run the deployment script.
```

## Prompt 3: Verify Deployment

```
Check the status of App Service 'BaynunahHRPortal' in resource group 'BaynunahHR':
- Is it running?
- Is VNet integration active?
- Are the environment variables configured?
- Show recent logs
- Provide the app URL
```

## Prompt 4: Troubleshoot Issues

```
App Service 'BaynunahHRPortal' is not starting. Help me diagnose:
1. Check application logs for errors
2. Verify database connectivity from App Service
3. Check if environment variables are set
4. Verify VNet integration is working
5. Suggest fixes for any issues found
```

## Prompt 5: Run Database Migrations

```
Connect to App Service 'BaynunahHRPortal' via SSH and run these commands:
cd /home/site/wwwroot
python -m alembic upgrade head

Show me the output.
```

---

## Quick Deployment Workflow

### Option A: Using Copilot (Most Automated)

1. **In Azure Portal, ask Copilot:**

   ```
   Complete HR Portal deployment setup for resource group 'BaynunahHR':
   - Reset PostgreSQL password (server: baynunahhrportal-server, admin: uutfqkhm)
   - Create database 'hrportal'
   - Configure VNet integration for App Service 'BaynunahHRPortal'
   Provide the password when done.
   ```

2. **In local terminal with password from Copilot:**

   ```bash
   chmod +x scripts/deploy_automated.sh
   ./scripts/deploy_automated.sh 'password_from_copilot'
   ```

3. **Ask Copilot to verify:**
   ```
   Verify HR Portal deployment at BaynunahHRPortal.azurewebsites.net
   ```

### Option B: Using Automation Script Only

1. **Get PostgreSQL password:**

   - Azure Portal → baynunahhrportal-server → Reset password
   - Save the password (username: uutfqkhm)

2. **Run deployment:**
   ```bash
   chmod +x scripts/deploy_automated.sh
   ./scripts/deploy_automated.sh 'your_password_here'
   ```

That's it! The script handles everything automatically.

---

## What the Automated Script Does

✅ Creates App Service subnet in VNet  
✅ Enables VNet integration on App Service  
✅ Creates PostgreSQL database  
✅ Builds React frontend  
✅ Packages backend with frontend  
✅ Configures all environment variables  
✅ Deploys to Azure App Service  
✅ Attempts to run database migrations

**Time:** ~5 minutes total

---

## Manual Fallback (If Automation Fails)

### 1. PostgreSQL Setup

```bash
# Reset password (Azure Portal or CLI)
az postgres flexible-server update \
  --name baynunahhrportal-server \
  --resource-group BaynunahHR \
  --admin-password 'NewPassword123!'

# Create database
az postgres flexible-server db create \
  --server-name baynunahhrportal-server \
  --resource-group BaynunahHR \
  --database-name hrportal
```

### 2. VNet Integration

```bash
# Create subnet
az network vnet subnet create \
  --resource-group BaynunahHR \
  --vnet-name BaynunahHRPortalVnet \
  --name AppServiceSubnet \
  --address-prefixes 10.0.1.0/24 \
  --delegations Microsoft.Web/serverFarms

# Enable integration
az webapp vnet-integration add \
  --name BaynunahHRPortal \
  --resource-group BaynunahHR \
  --vnet BaynunahHRPortalVnet \
  --subnet AppServiceSubnet
```

### 3. Deploy

```bash
./scripts/deploy_automated.sh 'your_password'
```
