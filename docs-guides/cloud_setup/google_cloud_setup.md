# Google Cloud Platform (GCP) Setup Guide

This guide provides step-by-step instructions for setting up a Google Cloud Platform account for GradientLab.

## 1. Create a Google Cloud Account

1. Visit the [Google Cloud website](https://cloud.google.com/free)
2. Click "Get started for free"
3. Sign in with your Google account or create a new one
4. Fill out the registration form, including your payment information (required for verification, but you won't be charged for free tier resources)
5. Complete the registration process

## 2. Set Up a GCP Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Click on the project dropdown at the top of the page
3. Click "New Project"
4. Name it "GradientLab" and select an organization if applicable
5. Click "Create"
6. Note the Project ID (you'll need this later)

## 3. Enable Required APIs

1. Navigate to "APIs & Services" > "Library"
2. Search for and enable the following APIs:
   - Compute Engine API
   - Cloud Resource Manager API
   - Identity and Access Management (IAM) API
   - Cloud Billing API

## 4. Create a Service Account

1. Navigate to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name it "gradientlab-automation" and provide a description
4. Click "Create and Continue"
5. Add the following roles:
   - Compute Admin
   - Service Account User
   - Storage Admin
6. Click "Continue" and then "Done"

## 5. Generate a Service Account Key

1. Find the service account you just created in the list
2. Click the three dots menu on the right and select "Manage keys"
3. Click "Add Key" > "Create new key"
4. Select "JSON" as the key type
5. Click "Create"
6. The key file will be downloaded automatically (keep this file secure)

## 6. Set Up Google Cloud CLI (Optional)

If you want to use the Google Cloud CLI locally:

1. Install the Google Cloud SDK:
   - [Windows](https://cloud.google.com/sdk/docs/install-sdk#windows)
   - [macOS](https://cloud.google.com/sdk/docs/install-sdk#mac)
   - [Linux](https://cloud.google.com/sdk/docs/install-sdk#linux)

2. Initialize the SDK:
   ```bash
   gcloud init
   ```

3. Authenticate with your Google account:
   ```bash
   gcloud auth login
   ```

4. Set the default project:
   ```bash
   gcloud config set project your-project-id
   ```

## 7. Configure GCP for GradientLab

1. Place the downloaded service account key file in a secure location in your GradientLab directory
2. Update the `vm_config.json` file with your GCP details:
   ```json
   {
     "google": {
       "num_vms": 1,
       "project_id": "your-project-id",
       "zone": "us-central1-a"
     },
     ...
   }
   ```
3. Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your service account key file:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
   ```

## 8. Verify Your Setup

1. Test your configuration with the Google Cloud CLI:
   ```bash
   gcloud compute instances list
   ```
2. If successful, you should see an empty list or any existing instances

## 9. Set Up Free Tier Resources

Google Cloud Free Tier includes:
- 1 e2-micro VM instance per month (in us-west1, us-central1, us-east1, us-east4, or us-south1)
- 30 GB of standard persistent disk storage per month
- 1 GB of outgoing network traffic from North America to all regions per month
- Many other services with free tier limits

These resources are sufficient for running a Gradient Sentry Node.

## 10. Next Steps

After setting up your Google Cloud account, proceed to:
1. Update the `vm_config.json` file with your Google Cloud details
2. Run the VM provisioning script to create VMs on Google Cloud
3. Set up the Sentry Node extension on the VMs

## Troubleshooting

### Service Account Key Issues
- Make sure the key file is in JSON format
- Ensure the environment variable points to the correct file
- Verify the service account has the necessary permissions

### API Enablement Issues
- Check that all required APIs are enabled
- It may take a few minutes for API enablement to propagate

### Resource Limits
- Free tier has resource limits; check the Google Cloud documentation for details
- If you need more resources, you may need to upgrade to a paid account

### Billing Issues
- Ensure your billing account is set up correctly
- Check that your billing account is linked to your project
