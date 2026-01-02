# Azure App Service Deployment Script (for non-technical users)
# This script uses Azure CLI. You can run it in Azure Cloud Shell (no install needed):
# https://shell.azure.com

# Set variables (edit these as needed)
RESOURCE_GROUP="secure-renewals-rg"
APP_SERVICE_PLAN="secure-renewals-plan"
WEBAPP_NAME="secure-renewals-app"
LOCATION="eastus"
GITHUB_REPO="ismaelloveexcel/Secure-Renewals-2"
BRANCH="main"

# 1. Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Create App Service plan
az appservice plan create --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP --sku B1 --is-linux

# 3. Create Web App (Python 3.11)
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_SERVICE_PLAN --name $WEBAPP_NAME --runtime "PYTHON|3.11"

# 4. Configure GitHub deployment
az webapp deployment source config --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --repo-url https://github.com/$GITHUB_REPO --branch $BRANCH --manual-integration

# 5. Set environment variables (edit/add as needed)
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --settings DATABASE_URL="<your-db-url>" AUTH_SECRET_KEY="<your-secret-key>"

# 6. Set startup command for FastAPI
az webapp config set --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app"

# 7. (Optional) SSH into the app and run Alembic migrations
# az webapp ssh --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME
# alembic upgrade head

# 8. Done! Your app will be live at: https://$WEBAPP_NAME.azurewebsites.net
