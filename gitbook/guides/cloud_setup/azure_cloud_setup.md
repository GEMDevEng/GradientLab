# Microsoft Azure Setup Guide

This guide provides step-by-step instructions for setting up a Microsoft Azure account for GradientLab.

## 1. Create an Azure Account

1. Visit the [Azure website](https://azure.microsoft.com/en-us/free/)
2. Click "Start free"
3. Sign in with your Microsoft account or create a new one
4. Fill out the registration form, including your payment information (required for verification, but you won't be charged for free tier resources)
5. Complete the registration process

## 2. Set Up an Azure Subscription

After registration, you'll have a subscription called "Azure subscription 1" or similar.

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

1. Navigate to "Azure Active Directory" > "App registrations"
2. Click "New registration"
3. Name it "gradientlab-automation"
4. Select "Accounts in this organizational directory only" for supported account types
5. Leave the redirect URI blank
6. Click "Register"
7. Note the Application (client) ID and Directory (tenant) ID (you'll need these later)

## 5. Create a Client Secret

1. In the app registration, navigate to "Certificates & secrets"
2. Click "New client secret"
3. Add a description and select an expiration period
4. Click "Add"
5. Note the client secret value (you'll need this later and won't be able to see it again)

## 6. Assign Permissions

1. Navigate to "Resource groups" and select the "GradientLab" resource group
2. Click "Access control (IAM)" in the left sidebar
3. Click "Add" > "Add role assignment"
4. Select the "Contributor" role
5. In the "Select" field, search for and select "gradientlab-automation"
6. Click "Save"

## 7. Set Up Azure CLI (Optional)

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

## 8. Configure Azure for GradientLab

1. Update the `vm_config.json` file with your Azure details:
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

2. Set the following environment variables:
   ```bash
   export AZURE_SUBSCRIPTION_ID="your-subscription-id"
   export AZURE_CLIENT_ID="your-client-id"
   export AZURE_CLIENT_SECRET="your-client-secret"
   export AZURE_TENANT_ID="your-tenant-id"
   ```

## 9. Verify Your Setup

1. Test your configuration with the Azure CLI:
   ```bash
   az vm list --resource-group GradientLab
   ```
2. If successful, you should see an empty list or any existing VMs

## 10. Set Up Free Tier Resources

Azure Free Tier includes:
- $200 credit for the first 30 days
- 12 months of free services, including:
  - 2 Linux or Windows B1s virtual machines (1 vCPU, 1 GB RAM)
  - 64 GB of standard SSD storage
  - 5 GB of bandwidth per month
- Many other services with free tier limits

These resources are sufficient for running a Gradient Sentry Node.

## 11. Next Steps

After setting up your Azure account, proceed to:
1. Update the `vm_config.json` file with your Azure details
2. Run the VM provisioning script to create VMs on Azure
3. Set up the Sentry Node extension on the VMs

## Troubleshooting

### Service Principal Issues
- Make sure the client secret is correct
- Ensure the service principal has the necessary permissions
- Verify the tenant ID and client ID

### Resource Group Issues
- Check that the resource group exists
- Ensure the service principal has Contributor access to the resource group

### Resource Limits
- Free tier has resource limits; check the Azure documentation for details
- If you need more resources, you may need to upgrade to a paid account

### Region Availability
- Not all resources are available in all regions
- Check the Azure region availability for the resources you need
