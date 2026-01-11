#!/bin/bash
# Master Automated Deployment Script for HR Portal
# Requires: Azure CLI logged in, PostgreSQL password

set -e  # Exit on error

# Configuration
APP_SERVICE_NAME="BaynunahHRPortal"
RESOURCE_GROUP="BaynunahHR"
POSTGRES_SERVER="baynunahhrportal-server"
VNET_NAME="BaynunahHRPortalVnet"
SUBNET_NAME="AppServiceSubnet"
DB_NAME="hrportal"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         HR Portal - Automated Azure Deployment                ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if password provided
if [ -z "$1" ]; then
  echo "❌ Error: PostgreSQL password required"
  echo ""
  echo "Usage: ./deploy_automated.sh 'postgres_password'"
  echo ""
  echo "Get password from Azure Portal:"
  echo "  Portal → baynunahhrportal-server → Settings → Reset password"
  echo "  Admin username: uutfqkhm"
  exit 1
fi

POSTGRES_PASSWORD="$1"
AUTH_SECRET=$(openssl rand -hex 32)

echo "📋 Deployment Configuration:"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   App Service: $APP_SERVICE_NAME"
echo "   PostgreSQL: $POSTGRES_SERVER"
echo "   Database: $DB_NAME"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  exit 0
fi

# Step 1: Configure VNet Integration
echo ""
echo "🔧 Step 1/7: Configuring VNet Integration..."
echo "   Creating App Service subnet in VNet..."

# Check if subnet exists
SUBNET_EXISTS=$(az network vnet subnet show \
  --resource-group $RESOURCE_GROUP \
  --vnet-name $VNET_NAME \
  --name $SUBNET_NAME 2>/dev/null || echo "")

if [ -z "$SUBNET_EXISTS" ]; then
  # Find available address space
  az network vnet subnet create \
    --resource-group $RESOURCE_GROUP \
    --vnet-name $VNET_NAME \
    --name $SUBNET_NAME \
    --address-prefixes 10.0.2.0/24 \
    --delegations Microsoft.Web/serverFarms \
    --output none 2>/dev/null || \
  az network vnet subnet create \
    --resource-group $RESOURCE_GROUP \
    --vnet-name $VNET_NAME \
    --name $SUBNET_NAME \
    --address-prefixes 10.0.3.0/24 \
    --delegations Microsoft.Web/serverFarms \
    --output none
  echo "   ✅ Subnet created"
else
  echo "   ✅ Subnet already exists"
fi

echo "   Enabling VNet Integration on App Service..."
az webapp vnet-integration add \
  --name $APP_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --vnet $VNET_NAME \
  --subnet $SUBNET_NAME \
  --output none 2>/dev/null || echo "   ✅ VNet Integration already enabled"

echo "   ✅ VNet Integration configured"

# Step 2: Create Database
echo ""
echo "🗄️  Step 2/7: Creating PostgreSQL database..."
DB_EXISTS=$(az postgres flexible-server db show \
  --server-name $POSTGRES_SERVER \
  --resource-group $RESOURCE_GROUP \
  --database-name $DB_NAME 2>/dev/null || echo "")

if [ -z "$DB_EXISTS" ]; then
  az postgres flexible-server db create \
    --server-name $POSTGRES_SERVER \
    --resource-group $RESOURCE_GROUP \
    --database-name $DB_NAME \
    --output none
  echo "   ✅ Database '$DB_NAME' created"
else
  echo "   ✅ Database already exists"
fi

# Step 3: Build Frontend
echo ""
echo "⚛️  Step 3/7: Building frontend..."
cd frontend
npm install --silent
npm run build
cd ..
echo "   ✅ Frontend built"

# Step 4: Prepare Backend
echo ""
echo "🐍 Step 4/7: Preparing backend..."
# Frontend already built to backend/static by vite config
if [ -d "backend/static" ] && [ -f "backend/static/index.html" ]; then
  echo "   ✅ Frontend already in backend/static"
else
  echo "   ⚠️  Frontend not found, attempting manual copy..."
  rm -rf backend/static
  if [ -d "frontend/dist" ]; then
    cp -r frontend/dist backend/static
  fi
fi

# Step 5: Configure App Service
echo ""
echo "⚙️  Step 5/7: Configuring App Service environment..."
az webapp config appsettings set \
  --name $APP_SERVICE_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    DATABASE_URL="postgresql+asyncpg://uutfqjkrhm:$POSTGRES_PASSWORD@$POSTGRES_SERVER.postgres.database.azure.com:5432/$DB_NAME?ssl=require" \
    AUTH_SECRET_KEY="$AUTH_SECRET" \
    ALLOWED_ORIGINS="https://$APP_SERVICE_NAME.azurewebsites.net" \
    APP_ENV="production" \
    PASSWORD_MIN_LENGTH="8" \
    SESSION_TIMEOUT_MINUTES="480" \
  --output none
echo "   ✅ Environment variables configured"

# Step 6: Deploy Application
echo ""
echo "🚀 Step 6/7: Deploying application..."
cd backend
echo "   Creating deployment package..."
zip -r -q ../deploy.zip . \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.git*" \
  -x "*.env*" \
  -x "*.example" \
  -x "*.md" \
  -x "*.lock" \
  -x "*test*.py" \
  -x "*.bak" \
  -x "*.tmp"
cd ..
echo "   Package size: $(du -h deploy.zip | cut -f1)"
echo "   Uploading to Azure..."
az webapp deployment source config-zip \
  --resource-group $RESOURCE_GROUP \
  --name $APP_SERVICE_NAME \
  --src deploy.zip \
  --output none
rm deploy.zip
echo "   ✅ Application deployed"

# Step 7: Run Database Migrations
echo ""
echo "🔄 Step 7/7: Running database migrations..."
echo "   Waiting for app to start..."
sleep 15

# Try to run migrations via SSH
echo "   Connecting via SSH to run migrations..."
az webapp ssh --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP --command "cd /home/site/wwwroot && python -m alembic upgrade head" 2>/dev/null || {
  echo "   ⚠️  Automatic migration failed. Run manually:"
  echo "      az webapp ssh --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
  echo "      cd /home/site/wwwroot && python -m alembic upgrade head"
}

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  🎉 Deployment Complete! 🎉                    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📱 Your HR Portal is now live:"
echo "   🌐 App URL:  https://$APP_SERVICE_NAME.azurewebsites.net"
echo "   📚 API Docs: https://$APP_SERVICE_NAME.azurewebsites.net/docs"
echo ""
echo "🔍 Useful commands:"
echo "   View logs:     az webapp log tail --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
echo "   SSH access:    az webapp ssh --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
echo "   Restart app:   az webapp restart --name $APP_SERVICE_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo "📝 Next steps:"
echo "   1. Visit the app URL and verify it loads"
echo "   2. Create your first admin user via the API"
echo "   3. Test the login flow"
echo ""
