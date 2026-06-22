#!/bin/bash

# Variables (replace with your values if needed)
RESOURCE_GROUP="azuredevops"
APP_NAME="hu-ml-app-3"
LOCATION="westeurope"


az login

# Create resource group
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION

# Create App Service plan
az appservice plan create \
  --name ${APP_NAME}-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux

# Create Web App (Python runtime)
az webapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan ${APP_NAME}-plan \
  --runtime "PYTHON|3.9"

# Configure deployment from GitHub
az webapp deployment source config \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --repo-url https://github.com/Hu-in/Azure_Cloud.git \
  --branch main \
  --manual-integration

# Show app URL
az webapp browse \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP
