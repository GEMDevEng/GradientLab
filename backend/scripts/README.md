# GradientLab Scripts

This directory contains scripts for automating various tasks related to the GradientLab project.

## VM Provisioning Scripts

### provision_oracle_vm.py

Provisions a VM on Oracle Cloud Infrastructure (OCI) using the OCI Python SDK.

```bash
./provision_oracle_vm.py --config /path/to/config.json --compartment-id ocid1.compartment.oc1.. --display-name GradientLab-VM-1
```

### provision_google_vm.py

Provisions a VM on Google Cloud Platform (GCP) using the Google Cloud SDK.

```bash
./provision_google_vm.py --project-id your-project-id --zone us-central1-a --instance-name gradientlab-vm-1 --machine-type e2-micro
```

### provision_azure_vm.py

Provisions a VM on Microsoft Azure using the Azure SDK for Python.

```bash
./provision_azure_vm.py --subscription-id your-subscription-id --resource-group GradientLab-RG --location eastus --vm-name gradientlab-vm-1 --vm-size Standard_B1s
```

## Node Setup Scripts

### setup_vm.sh

Sets up a VM for running Gradient Sentry Nodes. This script installs all necessary software and configures the VM.

```bash
sudo ./setup_vm.sh
```

### install_sentry_node.py

Installs the Gradient Sentry Node extension on a VM. This script connects to the VM via SSH and installs the extension.

```bash
./install_sentry_node.py 192.168.1.1 --username ubuntu --key-file /path/to/key.pem
```

## Monitoring Scripts

### monitor_nodes.py

Monitors Gradient Sentry Nodes. This script checks the status of all nodes and sends alerts if any are down.

```bash
./monitor_nodes.py --nodes-file nodes.json --username ubuntu --key-file /path/to/key.pem --smtp-server smtp.gmail.com --smtp-port 587 --smtp-username your-email@gmail.com --smtp-password your-password --from-email your-email@gmail.com --to-email your-email@gmail.com
```

### perform_poc_tap.py

Performs POC taps on Gradient Sentry Nodes. This script connects to each node and performs a POC tap.

```bash
./perform_poc_tap.py --nodes-file nodes.json --username ubuntu --key-file /path/to/key.pem
```

## Data Collection Scripts

### collect_rewards.py

Collects reward data from the Gradient Network. This script queries the Gradient Network API for reward data and stores it in a database.

```bash
./collect_rewards.py --nodes-file nodes.json --db-file rewards.db --api-url https://api.gradient.network --api-key your-api-key --days 7
```

### analyze_data.py

Analyzes the collected data from the Gradient Network. This script generates reports and insights from the collected data.

```bash
./analyze_data.py --nodes-file nodes.json --db-file rewards.db --output-dir reports
```

## Environment Variables

The scripts use the following environment variables:

- `OCI_USER_OCID`: Oracle Cloud Infrastructure user OCID
- `OCI_FINGERPRINT`: Oracle Cloud Infrastructure API key fingerprint
- `OCI_TENANCY_OCID`: Oracle Cloud Infrastructure tenancy OCID
- `OCI_REGION`: Oracle Cloud Infrastructure region
- `OCI_KEY_FILE`: Path to Oracle Cloud Infrastructure API key file
- `OCI_COMPARTMENT_OCID`: Oracle Cloud Infrastructure compartment OCID
- `OCI_SSH_PUBLIC_KEY`: SSH public key for Oracle Cloud Infrastructure VMs
- `GCP_SSH_PUBLIC_KEY`: SSH public key for Google Cloud Platform VMs
- `AZURE_SUBSCRIPTION_ID`: Microsoft Azure subscription ID
- `AZURE_SSH_PUBLIC_KEY`: SSH public key for Microsoft Azure VMs

## Dependencies

The scripts require the following dependencies:

- Python 3.6+
- OCI SDK: `pip install oci`
- Google Cloud SDK: `pip install google-cloud-compute google-auth`
- Azure SDK: `pip install azure-identity azure-mgmt-resource azure-mgmt-network azure-mgmt-compute`
- Pandas: `pip install pandas`
- Matplotlib: `pip install matplotlib`
- Requests: `pip install requests`

## Notes

- The scripts are designed to work with the free tier resources of each cloud provider.
- The scripts log their output to log files in the current directory.
- The scripts are designed to be run from the command line or as part of a scheduled job.
- The scripts are designed to be idempotent, so they can be run multiple times without causing issues.
