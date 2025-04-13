# Gradient Sentry Node Setup Guide

This guide provides instructions for setting up and configuring Gradient Sentry Nodes on your provisioned VMs.

## What is a Gradient Sentry Node?

A Gradient Sentry Node is a specialized node that participates in the Gradient Network by:

1. **Performing Proof of Activity (POA)** - Demonstrating active participation in the network
2. **Executing Proof of Contribution (POC) taps** - Validating contributions to the network
3. **Earning rewards** - Receiving tokens for successful POA and POC activities

## Prerequisites

Before setting up Sentry Nodes, ensure you have:

1. Provisioned VMs on one or more cloud providers
2. Generated an SSH key pair for accessing the VMs
3. Updated the `nodes.json` file with your VM details
4. Obtained a Gradient Network API key

## Automatic Setup

The VM provisioning process automatically sets up Sentry Nodes on each VM. If you used the `./deploy.sh vms` command, your Sentry Nodes should already be configured and running.

To verify the automatic setup:

1. Check the node status:
   ```bash
   python backend/scripts/monitor_nodes.py --nodes-file nodes.json
   ```

2. Access the status page:
   Open `http://<vm-ip-address>` in your browser to view the node status.

## Manual Setup

If you need to manually set up a Sentry Node on a VM:

1. Connect to the VM:
   ```bash
   ssh -i gradient_ssh_key username@ip-address
   ```
   The username depends on the cloud provider:
   - Oracle Cloud: `opc`
   - Google Cloud: `ubuntu`
   - Azure: `azureuser`

2. Download the setup script:
   ```bash
   wget https://raw.githubusercontent.com/GEMDevEng/GradientLab/main/backend/scripts/setup_vm.sh
   ```

3. Make the script executable:
   ```bash
   chmod +x setup_vm.sh
   ```

4. Run the setup script:
   ```bash
   sudo ./setup_vm.sh
   ```

5. Verify the installation:
   ```bash
   systemctl status chromium
   ```

## Sentry Node Components

A Gradient Sentry Node consists of the following components:

1. **Headless Chromium Browser**
   - Runs in the background
   - Executes POA and POC activities
   - Managed by a systemd service

2. **Xvfb (X Virtual Frame Buffer)**
   - Provides a virtual display for Chromium
   - Allows Chromium to run in headless mode
   - Managed by a systemd service

3. **Monitoring Scripts**
   - Check the status of the Sentry Node
   - Restart components if they fail
   - Send alerts if issues are detected

4. **Status Page**
   - Displays node status and metrics
   - Accessible via HTTP on port 80
   - Updated every minute

## Configuration

The Sentry Node configuration is stored in the following files:

1. `/home/gradient/sentry/config.json` - Main configuration file
2. `/etc/systemd/system/chromium.service` - Chromium service configuration
3. `/etc/systemd/system/xvfb.service` - Xvfb service configuration

To modify the configuration:

1. Connect to the VM
2. Edit the configuration files as needed
3. Restart the services:
   ```bash
   sudo systemctl restart xvfb
   sudo systemctl restart chromium
   ```

## Monitoring

The Sentry Node includes built-in monitoring:

1. **Local Monitoring**
   - Cron job that checks the status every 5 minutes
   - Automatically restarts components if they fail
   - Logs issues to `/home/gradient/sentry/monitor.log`

2. **Remote Monitoring**
   - The `monitor_nodes.py` script checks all nodes
   - Sends alerts if nodes are down
   - Attempts to restart nodes remotely

3. **Status Page**
   - Displays real-time status and metrics
   - Shows uptime, CPU usage, memory usage, and disk usage
   - Updates every minute

## Troubleshooting

### Chromium Not Running

If Chromium is not running:

1. Check the service status:
   ```bash
   sudo systemctl status chromium
   ```

2. Check the logs:
   ```bash
   sudo journalctl -u chromium
   ```

3. Restart the service:
   ```bash
   sudo systemctl restart chromium
   ```

### POC Taps Not Working

If POC taps are not working:

1. Check the POC tap logs:
   ```bash
   cat /home/gradient/sentry/poc_tap.log
   ```

2. Run a manual POC tap:
   ```bash
   sudo /home/gradient/sentry/poc_tap.sh
   ```

3. Check the Gradient Network API connection:
   ```bash
   curl -I https://api.gradient.network
   ```

### Status Page Not Accessible

If the status page is not accessible:

1. Check the Nginx service:
   ```bash
   sudo systemctl status nginx
   ```

2. Check the Nginx configuration:
   ```bash
   sudo nginx -t
   ```

3. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

## Next Steps

After setting up your Sentry Nodes, proceed to:

1. [Configure scheduled tasks](../scheduled_tasks/README.md)
2. [Set up data collection](../data_collection/README.md)
3. [Analyze rewards and performance](../data_analysis/README.md)
