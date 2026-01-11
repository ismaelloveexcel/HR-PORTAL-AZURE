# HR Portal Deployment - Simple Step-by-Step Guide

Follow these steps in order. Copy and paste each command.

## Step 1: Get PostgreSQL Password (Manual - 2 minutes)

### Generate a strong password:

```bash
chmod +x scripts/generate_postgres_password.sh
./scripts/generate_postgres_password.sh
```

Copy the generated password, then:

1. Go to Azure Portal: https://portal.azure.com
2. Search for "baynunahhrportal-server"
3. Click on it
4. In left menu: Settings → **Reset password**
5. Paste the generated password
6. Username is: **uutfqkhm**
7. Save the password somewhere safe

**Password Requirements:**

- Must contain 3 of 4: uppercase, lowercase, numbers, special chars (!$#% etc.)
- Cannot contain username or parts of it
- Minimum 8 characters (we generate 16)

## Step 2: Run Automated Deployment (5 minutes)

Open your terminal in this project directory and run:

```bash
# Make script executable
chmod +x scripts/deploy_automated.sh

# Run deployment (replace YOUR_PASSWORD with the password from Step 1)
./scripts/deploy_automated.sh 'YOUR_PASSWORD'
```

**That's it!** The script will:

- Configure VNet integration
- Create database
- Build frontend
- Deploy everything
- Run migrations

## Step 3: Verify Deployment

After deployment completes, visit:

- **App:** https://BaynunahHRPortal.azurewebsites.net
- **API Docs:** https://BaynunahHRPortal.azurewebsites.net/docs

## Troubleshooting

### If deployment fails:

**Check logs:**

```bash
az webapp log tail --name BaynunahHRPortal --resource-group BaynunahHR
```

**Restart app:**

```bash
az webapp restart --name BaynunahHRPortal --resource-group BaynunahHR
```

**Run migrations manually:**

```bash
az webapp ssh --name BaynunahHRPortal --resource-group BaynunahHR
cd /home/site/wwwroot
python -m alembic upgrade head
exit
```

## Need Help?

If something fails, check the error message and:

1. Verify you're logged into Azure CLI: `az login`
2. Verify password is correct
3. Check the logs command above

---

**Total Time: ~7 minutes**

- Step 1 (Manual): 2 minutes
- Step 2 (Automated): 5 minutes
- Step 3 (Verify): 1 minute
