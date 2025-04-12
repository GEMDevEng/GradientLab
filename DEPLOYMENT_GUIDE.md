# GradientLab Deployment Guide

This guide provides step-by-step instructions for deploying the GradientLab application, provisioning VMs, and setting up data collection.

## Prerequisites

1. **Cloud Provider Accounts**
   - Oracle Cloud Infrastructure account
   - Google Cloud Platform account
   - Microsoft Azure account

2. **API Keys and Credentials**
   - Oracle Cloud API key and config file
   - Google Cloud credentials
   - Azure credentials
   - Gradient Network API key

3. **Tools**
   - Git
   - Node.js and npm
   - Python 3.9+
   - Heroku CLI
   - jq (for JSON processing)

## Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/GEMDevEng/GradientLab.git
cd GradientLab
```

### 2. Deploy the Backend to Heroku

```bash
# Deploy the backend to Heroku
./deploy.sh backend
```

This will:
- Create a Heroku app
- Add PostgreSQL add-on
- Set environment variables
- Deploy the backend code
- Initialize the database

### 3. Deploy the Frontend to GitHub Pages

```bash
# Deploy the frontend to GitHub Pages
./deploy.sh frontend
```

This will:
- Install dependencies
- Build the React application
- Deploy to GitHub Pages

### 4. Configure VM Provisioning

Edit the `vm_config.json` file with your cloud provider credentials:

```json
{
    "oracle": {
        "num_vms": 1,
        "compartment_id": "ocid1.compartment.oc1..example",
        "config_file": "oracle_config.json"
    },
    "google": {
        "num_vms": 1,
        "project_id": "your-google-project-id",
        "zone": "us-central1-a"
    },
    "azure": {
        "num_vms": 1,
        "subscription_id": "your-azure-subscription-id",
        "location": "eastus"
    },
    "ssh_key_file": "gradient_ssh_key",
    "nodes_file": "nodes.json"
}
```

### 5. Provision VMs

```bash
# Provision VMs on all cloud providers
./deploy.sh vms
```

This will:
- Provision VMs on Oracle Cloud, Google Cloud, and Azure
- Install necessary software on the VMs
- Install the Sentry Node extension
- Save VM details to the nodes file

### 6. Configure Scheduled Tasks

Edit the `tasks_config.json` file with your configuration:

```json
{
    "nodes_file": "nodes.json",
    "db_file": "rewards.db",
    "output_dir": "reports",
    "api_url": "https://api.gradient.network",
    "api_key": "your-gradient-api-key",
    "username": "ubuntu",
    "key_file": "gradient_ssh_key",
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587,
        "username": "your-email@gmail.com",
        "password": "your-app-password",
        "from": "your-email@gmail.com",
        "to": "your-email@gmail.com"
    }
}
```

### 7. Set Up Scheduled Tasks

```bash
# Set up scheduled tasks for monitoring and data collection
./deploy.sh tasks
```

This will:
- Set up cron jobs for monitoring nodes
- Set up cron jobs for performing POC taps
- Set up cron jobs for collecting rewards
- Set up cron jobs for analyzing data

### 8. Deploy Everything at Once

Alternatively, you can deploy everything at once:

```bash
# Deploy everything
./deploy.sh all
```

## Monitoring and Management

### Checking Node Status

```bash
# Check the status of all nodes
python3 backend/scripts/monitor_nodes.py --nodes-file nodes.json
```

### Collecting Rewards Data

```bash
# Collect rewards data
python3 backend/scripts/collect_rewards.py --nodes-file nodes.json --db-file rewards.db --api-url https://api.gradient.network --api-key your-api-key
```

### Analyzing Data

```bash
# Analyze collected data
python3 backend/scripts/analyze_data.py --nodes-file nodes.json --db-file rewards.db --output-dir reports
```

## Troubleshooting

### VM Provisioning Issues

- **Oracle Cloud**: Check the OCI configuration file and compartment ID
- **Google Cloud**: Ensure the Google Cloud SDK is properly configured
- **Azure**: Verify the Azure credentials and subscription ID

### Node Monitoring Issues

- Check SSH connectivity to the VMs
- Verify that the Sentry Node extension is installed
- Check the node status page at http://<vm-ip>/

### Data Collection Issues

- Verify the Gradient Network API key
- Check the database file permissions
- Ensure the scheduled tasks are running

## Maintenance

### Updating the Application

```bash
# Pull the latest changes
git pull origin main

# Redeploy
./deploy.sh all
```

### Backing Up Data

```bash
# Backup the nodes file and rewards database
cp nodes.json nodes.json.bak
cp rewards.db rewards.db.bak
```

### Restoring Data

```bash
# Restore from backup
cp nodes.json.bak nodes.json
cp rewards.db.bak rewards.db
```
