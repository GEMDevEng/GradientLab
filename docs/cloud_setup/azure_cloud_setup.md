# Microsoft Azure Setup Guide

This guide provides step-by-step instructions for setting up a Microsoft Azure account for GradientLab.

## 1. Create a Microsoft Azure Account

1. Visit the [Azure website](https://azure.microsoft.com/en-us/free/)
2. Click "Start free"
3. Sign in with your Microsoft account or create a new one
4. Fill out the registration form, including your payment information (required for verification, but you won't be charged for free tier resources)
5. Complete the registration process

## 2. Set Up an Azure Subscription

After registration, you'll have a free subscription with $200 credit for 30 days.

1. Go to the [Azure Portal](https://portal.azure.com/)
2. Navigate to "Subscriptions" in the left sidebar
3. Note your Subscription ID (you'll need this later)

## 3. Create a Resource Group

1. Navigate to "Resource groups" in the left sidebar
2. Click "Create"
3. Select your subscription
4. Name the resource group "GradientLab"
5. Select a region (choose one close to you for better performance)
6. Click "Review + create" and then "Create"

## 4. Create a Service Principal

1. Open Azure Cloud Shell by clicking the terminal icon in the top navigation bar
2. Select "Bash" as the shell type
3. Run the following command to create a service principal:
   ```bash
   az ad sp create-for-rbac --name "GradientLabAutomation" --role Contributor --scopes /subscriptions/your-subscription-id/resourceGroups/GradientLab
   ```
4. Note the output, which includes:
   - `appId` (this is your client ID)
   - `password` (this is your client secret)
   - `tenant` (this is your tenant ID)

## 5. Set Up Azure CLI (Optional)

If you want to use the Azure CLI locally:

1. Install the Azure CLI:
   - [Windows](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows)
   - [macOS](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos)
   - [Linux](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux)

2. Log in to Azure:
   ```bash
   az login
   ```

3. Set the default subscription:
   ```bash
   az account set --subscription your-subscription-id
   ```

## 6. Configure Azure for GradientLab

1. Create a file named `azure_credentials.json` in the GradientLab root directory
2. Add the following content:
   ```json
   {
     "clientId": "your-client-id",
     "clientSecret": "your-client-secret",
     "subscriptionId": "your-subscription-id",
     "tenantId": "your-tenant-id",
     "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
     "resourceManagerEndpointUrl": "https://management.azure.com/",
     "activeDirectoryGraphResourceId": "https://graph.windows.net/",
     "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
     "galleryEndpointUrl": "https://gallery.azure.com/",
     "managementEndpointUrl": "https://management.core.windows.net/"
   }
   ```
3. Replace the placeholders with your actual values
4. Update the `vm_config.json` file with your Azure details:
   ```json
   {
     "azure": {
       "num_vms": 1,
       "subscription_id": "your-subscription-id",
       "location": "eastus"
     },
     ...
   }
   ```
5. Set the following environment variables:
   ```bash
   export AZURE_SUBSCRIPTION_ID="your-subscription-id"
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   export AZURE_TENANT_ID="your-tenant-id"
   ```

## 7. Verify Your Setup

1. Test your configuration with the Azure CLI:
   ```bash
   az vm list --resource-group GradientLab
   ```
2. If successful, you should see an empty list or any existing VMs

## 8. Set Up Free Tier Resources

Azure Free Tier includes:
- 12 months of popular free services
- $200 credit to explore any Azure service for 30 days
- 25+ services that are always free

For VMs, you can use:
- B1s (1 vCPU, 1 GB RAM) Linux VM for 750 hours per month for 12 months

These resources are sufficient for running a Gradient Sentry Node.

## 9. Next Steps

After setting up your Azure account, proceed to:
1. Update the `vm_config.json` file with your Azure details
2. Run the VM provisioning script to create VMs on Azure
3. Set up the Sentry Node extension on the VMs

## Troubleshooting

### Service Principal Issues
- If you get an error creating the service principal, make sure you have the necessary permissions
- You may need to be an Owner or User Access Administrator in your subscription

### Authentication Issues
- Make sure the client ID, client secret, and tenant ID are correct
- Ensure the environment variables are set correctly

### Resource Limits
- Free tier has resource limits; check the Azure documentation for details
- If you need more resources, you may need to upgrade to a paid account

### Region Availability
- Not all resources are available in all regions
- If you encounter region-specific issues, try a different region
