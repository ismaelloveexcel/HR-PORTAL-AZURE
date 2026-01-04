#!/bin/bash
# Azure Infrastructure Setup Script for Secure Renewals HR Portal
# 
# This script creates all required Azure resources for deploying the HR Portal.
# Run this in Azure Cloud Shell (https://shell.azure.com) or locally with Azure CLI installed.
#
# Usage:
#   chmod +x azure-setup.sh
#   ./azure-setup.sh
#
# Prerequisites:
#   - Azure CLI installed (az --version)
#   - Logged in to Azure (az login)
#   - Sufficient permissions to create resources

set -e

# ============================================================================
# Configuration - Edit these values as needed
# ============================================================================

RESOURCE_GROUP="${RESOURCE_GROUP:-secure-renewals-rg}"
LOCATION="${LOCATION:-eastus}"
APP_SERVICE_PLAN="${APP_SERVICE_PLAN:-secure-renewals-plan}"
BACKEND_APP="${BACKEND_APP:-secure-renewals-api}"
FRONTEND_APP="${FRONTEND_APP:-secure-renewals-app}"
PG_SERVER="${PG_SERVER:-secure-renewals-db}"
PG_ADMIN="${PG_ADMIN:-secureadmin}"
DATABASE="${DATABASE:-secure_renewals}"
APP_INSIGHTS="${APP_INSIGHTS:-secure-renewals-insights}"

# App Service SKU: F1 (Free), B1 (Basic), S1 (Standard), P1V2 (Premium)
APP_SERVICE_SKU="${APP_SERVICE_SKU:-B1}"

# PostgreSQL SKU: Standard_B1ms (Burstable), Standard_D2s_v3 (General Purpose)
PG_SKU="${PG_SKU:-Standard_B1ms}"
PG_TIER="${PG_TIER:-Burstable}"
PG_STORAGE="${PG_STORAGE:-32}"
PG_VERSION="${PG_VERSION:-15}"

# ============================================================================
# Helper Functions
# ============================================================================

print_header() {
    echo ""
    echo "=============================================="
    echo "$1"
    echo "=============================================="
}

print_success() {
    echo "✅ $1"
}

print_info() {
    echo "ℹ️  $1"
}

print_warning() {
    echo "⚠️  $1"
}

# ============================================================================
# Pre-flight Checks
# ============================================================================

print_header "Pre-flight Checks"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi
print_success "Azure CLI is installed"

# Check if logged in
if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure. Please run: az login"
    exit 1
fi
print_success "Logged in to Azure"

# Show current subscription
SUBSCRIPTION=$(az account show --query name -o tsv)
print_info "Using subscription: $SUBSCRIPTION"

# ============================================================================
# Generate PostgreSQL password
# ============================================================================

if [ -z "$PG_PASSWORD" ]; then
    # Use alphanumeric characters only to avoid URL encoding issues in connection strings
    PG_PASSWORD=$(openssl rand -base64 32 | tr -dc 'A-Za-z0-9' | head -c 24)
    print_warning "Generated PostgreSQL password. Save this securely!"
fi

# ============================================================================
# Create Resource Group
# ============================================================================

print_header "Creating Resource Group"

if az group show --name $RESOURCE_GROUP &> /dev/null; then
    print_info "Resource group '$RESOURCE_GROUP' already exists"
else
    az group create --name $RESOURCE_GROUP --location $LOCATION --output none
    print_success "Created resource group: $RESOURCE_GROUP"
fi

# ============================================================================
# Create App Service Plan
# ============================================================================

print_header "Creating App Service Plan"

if az appservice plan show --name $APP_SERVICE_PLAN --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_info "App Service Plan '$APP_SERVICE_PLAN' already exists"
else
    az appservice plan create \
        --name $APP_SERVICE_PLAN \
        --resource-group $RESOURCE_GROUP \
        --sku $APP_SERVICE_SKU \
        --is-linux \
        --output none
    print_success "Created App Service Plan: $APP_SERVICE_PLAN (SKU: $APP_SERVICE_SKU)"
fi

# ============================================================================
# Create Backend Web App
# ============================================================================

print_header "Creating Backend Web App"

if az webapp show --name $BACKEND_APP --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_info "Backend app '$BACKEND_APP' already exists"
else
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --name $BACKEND_APP \
        --runtime "PYTHON|3.11" \
        --output none
    print_success "Created backend app: $BACKEND_APP"
fi

# Configure backend startup command
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --startup-file "gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000" \
    --output none
print_success "Configured backend startup command"

# ============================================================================
# Create Frontend Web App
# ============================================================================

print_header "Creating Frontend Web App"

if az webapp show --name $FRONTEND_APP --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_info "Frontend app '$FRONTEND_APP' already exists"
else
    az webapp create \
        --resource-group $RESOURCE_GROUP \
        --plan $APP_SERVICE_PLAN \
        --name $FRONTEND_APP \
        --runtime "NODE|20-lts" \
        --output none
    print_success "Created frontend app: $FRONTEND_APP"
fi

# ============================================================================
# Create PostgreSQL Flexible Server
# ============================================================================

print_header "Creating PostgreSQL Database"

if az postgres flexible-server show --name $PG_SERVER --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_info "PostgreSQL server '$PG_SERVER' already exists"
else
    az postgres flexible-server create \
        --resource-group $RESOURCE_GROUP \
        --name $PG_SERVER \
        --admin-user $PG_ADMIN \
        --admin-password "$PG_PASSWORD" \
        --sku-name $PG_SKU \
        --tier $PG_TIER \
        --storage-size $PG_STORAGE \
        --version $PG_VERSION \
        --output none
    print_success "Created PostgreSQL server: $PG_SERVER"
fi

# Create database
if az postgres flexible-server db show --resource-group $RESOURCE_GROUP --server-name $PG_SERVER --database-name $DATABASE &> /dev/null; then
    print_info "Database '$DATABASE' already exists"
else
    az postgres flexible-server db create \
        --resource-group $RESOURCE_GROUP \
        --server-name $PG_SERVER \
        --database-name $DATABASE \
        --output none
    print_success "Created database: $DATABASE"
fi

# Allow Azure services to access PostgreSQL
# Note: 0.0.0.0-0.0.0.0 is Azure's documented pattern for allowing Azure services
# For enhanced security in production, consider using Private Link or VNet integration
# See: https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-firewall-rules
az postgres flexible-server firewall-rule create \
    --resource-group $RESOURCE_GROUP \
    --name $PG_SERVER \
    --rule-name AllowAzureServices \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0 \
    --output none 2>/dev/null || true
print_success "Configured PostgreSQL firewall for Azure services"

# ============================================================================
# Create Application Insights
# ============================================================================

print_header "Creating Application Insights"

if az monitor app-insights component show --app $APP_INSIGHTS --resource-group $RESOURCE_GROUP &> /dev/null; then
    print_info "Application Insights '$APP_INSIGHTS' already exists"
else
    az monitor app-insights component create \
        --app $APP_INSIGHTS \
        --location $LOCATION \
        --resource-group $RESOURCE_GROUP \
        --output none
    print_success "Created Application Insights: $APP_INSIGHTS"
fi

# Get connection string
INSIGHTS_CONNECTION=$(az monitor app-insights component show \
    --app $APP_INSIGHTS \
    --resource-group $RESOURCE_GROUP \
    --query connectionString \
    --output tsv)

# ============================================================================
# Configure Backend Environment Variables
# ============================================================================

print_header "Configuring Backend Environment Variables"

# Build database URL
DATABASE_URL="postgresql+asyncpg://${PG_ADMIN}:${PG_PASSWORD}@${PG_SERVER}.postgres.database.azure.com:5432/${DATABASE}?sslmode=require"

# Generate auth secret if not provided
AUTH_SECRET_KEY="${AUTH_SECRET_KEY:-$(openssl rand -hex 32)}"

# Set backend app settings
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $BACKEND_APP \
    --settings \
        DATABASE_URL="$DATABASE_URL" \
        AUTH_SECRET_KEY="$AUTH_SECRET_KEY" \
        ALLOWED_ORIGINS="https://${FRONTEND_APP}.azurewebsites.net" \
        APP_ENV="production" \
        LOG_LEVEL="INFO" \
        APPLICATIONINSIGHTS_CONNECTION_STRING="$INSIGHTS_CONNECTION" \
    --output none
print_success "Configured backend environment variables"

# ============================================================================
# Create Service Principal for GitHub Actions
# ============================================================================

print_header "Creating Service Principal for GitHub Actions"

SUBSCRIPTION_ID=$(az account show --query id -o tsv)
# Use timestamp for unique service principal name to avoid conflicts in shared tenants
SP_TIMESTAMP=$(date +%Y%m%d%H%M%S)
SP_NAME="secure-renewals-github-${SP_TIMESTAMP}"

SP_OUTPUT=$(az ad sp create-for-rbac \
    --name "$SP_NAME" \
    --role contributor \
    --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP" \
    --sdk-auth)

print_success "Created service principal: $SP_NAME"

# ============================================================================
# Summary
# ============================================================================

print_header "Setup Complete! 🎉"

echo ""
echo "📋 Resources Created:"
echo "   Resource Group:     $RESOURCE_GROUP"
echo "   Backend App:        https://${BACKEND_APP}.azurewebsites.net"
echo "   Frontend App:       https://${FRONTEND_APP}.azurewebsites.net"
echo "   PostgreSQL Server:  $PG_SERVER.postgres.database.azure.com"
echo "   Database:           $DATABASE"
echo "   Application Insights: $APP_INSIGHTS"
echo ""

print_header "GitHub Actions Secrets"
echo ""
echo "Add these secrets to your GitHub repository:"
echo "(Settings → Secrets and variables → Actions → New repository secret)"
echo ""
echo "1. AZURE_CREDENTIALS:"
echo "$SP_OUTPUT"
echo ""
echo "2. AZURE_RESOURCE_GROUP:"
echo "$RESOURCE_GROUP"
echo ""
echo "3. AZURE_WEBAPP_NAME_BACKEND:"
echo "$BACKEND_APP"
echo ""
echo "4. AZURE_WEBAPP_NAME_FRONTEND:"
echo "$FRONTEND_APP"
echo ""
echo "5. VITE_API_BASE_URL:"
echo "https://${BACKEND_APP}.azurewebsites.net/api"
echo ""

if [ -n "$PG_PASSWORD" ]; then
    print_header "⚠️ IMPORTANT: Save These Credentials Securely!"
    echo ""
    echo "PostgreSQL Admin:    $PG_ADMIN"
    echo "PostgreSQL Password: $PG_PASSWORD"
    echo "Auth Secret Key:     $AUTH_SECRET_KEY"
    echo ""
    echo "Database URL (for reference):"
    echo "$DATABASE_URL"
    echo ""
fi

echo "Next steps:"
echo "1. Add the GitHub secrets listed above"
echo "2. Push code to the main branch"
echo "3. GitHub Actions will automatically deploy your app!"
echo ""
