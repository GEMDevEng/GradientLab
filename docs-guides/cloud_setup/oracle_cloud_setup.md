# Oracle Cloud Infrastructure (OCI) Setup Guide

This guide provides step-by-step instructions for setting up an Oracle Cloud Infrastructure account for GradientLab.

## 1. Create an Oracle Cloud Account

1. Visit the [Oracle Cloud website](https://www.oracle.com/cloud/free/)
2. Click "Start for free"
3. Fill out the registration form with your information
4. Verify your email address and phone number
5. Enter your credit card information (required for verification, but you won't be charged for free tier resources)
6. Complete the registration process

## 2. Set Up Your Oracle Cloud Tenancy

After registration, you'll be directed to your Oracle Cloud dashboard.

1. Navigate to "Administration" > "Tenancy Details"
2. Note your Tenancy OCID (you'll need this later)
3. Navigate to "Identity" > "Compartments"
4. Click "Create Compartment"
5. Name it "GradientLab" and provide a description
6. Note the Compartment OCID (you'll need this later)

## 3. Create a User and Generate API Keys

1. Navigate to "Identity" > "Users"
2. Click "Create User"
3. Name it "gradientlab-automation" and provide a description
4. Click "Create"
5. Select the new user and click "API Keys" in the Resources section
6. Click "Add API Key"
7. Select "Generate API Key Pair"
8. Download both the private and public keys
9. Click "Add" to add the key to the user
10. Note the key fingerprint and the user OCID (you'll need these later)

## 4. Create Policies for the User

1. Navigate to "Identity" > "Policies"
2. Click "Create Policy"
3. Name it "GradientLabPolicy" and provide a description
4. Select the root compartment
5. Add the following policy statements:
   ```
   Allow user gradientlab-automation to manage all-resources in compartment GradientLab
   Allow user gradientlab-automation to read all-resources in tenancy
   ```
6. Click "Create"

## 5. Configure OCI CLI (Optional)

If you want to use the OCI CLI locally:

1. Install the OCI CLI:
   ```bash
   bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
   ```
2. Configure the CLI:
   ```bash
   oci setup config
   ```
3. Follow the prompts, providing your user OCID, tenancy OCID, region, and the path to your private key

## 6. Create an OCI Configuration File for GradientLab

1. Create a file named `oci_config.json` in the GradientLab root directory
2. Add the following content:
   ```json
   {
     "user": "your-user-ocid",
     "fingerprint": "your-key-fingerprint",
     "tenancy": "your-tenancy-ocid",
     "region": "your-region",
     "key_file": "path/to/your/private-key.pem"
   }
   ```
3. Replace the placeholders with your actual values
4. Update the `vm_config.json` file with your compartment OCID and config file path:
   ```json
   {
     "oracle": {
       "num_vms": 1,
       "compartment_id": "your-compartment-ocid",
       "config_file": "oci_config.json"
     },
     ...
   }
   ```

## 7. Verify Your Setup

1. Test your configuration with the OCI CLI:
   ```bash
   oci compute instance list --compartment-id your-compartment-ocid
   ```
2. If successful, you should see an empty list or any existing instances

## 8. Set Up Free Tier Resources

Oracle Cloud Free Tier includes:
- 2 AMD-based Compute VMs with 1/8 OCPU and 1 GB memory each
- 2 Block Volumes with 50 GB total storage
- 10 GB Object Storage
- 10 GB Archive Storage
- 1 Load Balancer instance with 10 Mbps bandwidth
- 1 Oracle Autonomous Database with 20 GB storage

These resources are sufficient for running Gradient Sentry Nodes.

## 9. Next Steps

After setting up your Oracle Cloud account, proceed to:
1. Update the `vm_config.json` file with your Oracle Cloud details
2. Run the VM provisioning script to create VMs on Oracle Cloud
3. Set up the Sentry Node extension on the VMs

## Troubleshooting

### API Key Issues
- Make sure the private key is in PEM format
- Ensure the key has the correct permissions (chmod 600)
- Verify the key fingerprint matches the one in the OCI console

### Permission Issues
- Check that the policy statements are correct
- Ensure the user has the necessary permissions for the compartment

### Resource Limits
- Free tier has resource limits; check the Oracle Cloud documentation for details
- If you need more resources, you may need to upgrade to a paid account
