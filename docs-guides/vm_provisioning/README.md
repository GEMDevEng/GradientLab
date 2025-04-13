# VM Provisioning Guide for GradientLab

This guide provides instructions for provisioning virtual machines (VMs) for GradientLab across multiple cloud providers.

## Prerequisites

Before provisioning VMs, ensure you have:

1. Set up accounts with the cloud providers you want to use
2. Configured authentication for each provider
3. Updated the `vm_config.json` file with your account details
4. Generated an SSH key pair for accessing the VMs

See the [Cloud Setup Guide](../cloud_setup/README.md) for details on these prerequisites.

## Provisioning Process

GradientLab provides scripts to automate VM provisioning across all supported cloud providers. The process involves:

1. **Configuration** - Setting up the VM configuration file
2. **Provisioning** - Running the provisioning script to create VMs
3. **Setup** - Installing necessary software on the VMs
4. **Verification** - Checking that the VMs are properly set up

## VM Configuration

The `vm_config.json` file in the root directory controls the VM provisioning process:

```json
{
    "oracle": {
        "num_vms": 1,
        "compartment_id": "your-compartment-ocid",
        "config_file": "oci_config.json"
    },
    "google": {
        "num_vms": 1,
        "project_id": "your-project-id",
        "zone": "us-central1-a"
    },
    "azure": {
        "num_vms": 1,
        "subscription_id": "your-subscription-id",
        "location": "eastus"
    },
    "ssh_key_file": "gradient_ssh_key",
    "nodes_file": "nodes.json"
}
```

Adjust the number of VMs for each provider based on your needs and available resources.

## Provisioning VMs

To provision VMs across all configured cloud providers:

```bash
./deploy.sh vms
```

This script will:
1. Read the configuration from `vm_config.json`
2. Provision VMs on each configured cloud provider
3. Install necessary software on each VM
4. Install the Sentry Node extension
5. Save VM details to the nodes file

## VM Specifications

The provisioning scripts create VMs with the following specifications:

### Oracle Cloud
- VM Type: VM.Standard.E2.1.Micro
- vCPUs: 1/8 OCPU
- RAM: 1 GB
- Storage: 50 GB
- OS: Oracle Linux 8

### Google Cloud
- VM Type: e2-micro
- vCPUs: 0.25 vCPU
- RAM: 1 GB
- Storage: 30 GB
- OS: Ubuntu 20.04 LTS

### Azure
- VM Type: B1s
- vCPUs: 1 vCPU
- RAM: 1 GB
- Storage: 64 GB
- OS: Ubuntu 18.04 LTS

## VM Setup

The provisioning process automatically sets up each VM with:

1. **Base Software**
   - Docker and Docker Compose
   - Node.js
   - Chromium browser
   - Monitoring tools

2. **Sentry Node Extension**
   - Installs the Gradient Sentry Node extension
   - Configures it to run automatically
   - Sets up monitoring and restart mechanisms

3. **Status Page**
   - Creates a simple status page accessible via HTTP
   - Displays node status, uptime, and resource usage

## Verifying VM Provisioning

After provisioning, verify that the VMs are properly set up:

1. **Check the nodes file**
   ```bash
   cat nodes.json
   ```
   This file contains details about all provisioned VMs.

2. **Check VM connectivity**
   ```bash
   python backend/scripts/monitor_nodes.py --nodes-file nodes.json
   ```
   This script checks the status of all nodes and reports any issues.

3. **Access the status page**
   Open `http://<vm-ip-address>` in your browser to view the node status page.

## Managing VMs

### Stopping VMs

To stop VMs when not in use (to save resources):

```bash
python backend/scripts/manage_vms.py --nodes-file nodes.json --action stop
```

### Starting VMs

To start previously stopped VMs:

```bash
python backend/scripts/manage_vms.py --nodes-file nodes.json --action start
```

### Deleting VMs

To delete VMs when they are no longer needed:

```bash
python backend/scripts/manage_vms.py --nodes-file nodes.json --action delete
```

## Troubleshooting

### Provisioning Failures

If VM provisioning fails:

1. Check the logs in `vm_provisioning.log`
2. Verify your cloud provider credentials
3. Ensure you have sufficient quota/resources available
4. Check for any region-specific issues

### Connection Issues

If you can't connect to a VM:

1. Verify the VM is running in the cloud provider console
2. Check that the security group/firewall allows SSH access
3. Ensure your SSH key is correct
4. Try connecting manually: `ssh -i gradient_ssh_key username@ip-address`

### Software Installation Issues

If software installation fails:

1. Connect to the VM manually
2. Check the installation logs in `/var/log/gradient_setup.log`
3. Try running the setup script manually: `sudo /tmp/setup_vm.sh`

## Next Steps

After provisioning VMs, proceed to:

1. [Set up scheduled tasks](../scheduled_tasks/README.md)
2. [Configure monitoring and alerts](../monitoring/README.md)
3. [Start collecting data](../data_collection/README.md)
