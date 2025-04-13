# Monitoring and Optimization Guide for GradientLab

This guide provides instructions for monitoring and optimizing Gradient Sentry Nodes to maximize performance and rewards.

## Monitoring Overview

GradientLab includes a comprehensive monitoring system that:

1. **Tracks node status** - Monitors uptime, resource usage, and connectivity
2. **Collects reward data** - Gathers information about POA, POC, and referral rewards
3. **Generates reports** - Creates performance reports and insights
4. **Sends alerts** - Notifies you of issues that require attention

## Monitoring Components

The monitoring system consists of the following components:

### 1. Node Monitoring

The `monitor_nodes.py` script checks the status of all nodes:

```bash
python backend/scripts/monitor_nodes.py --nodes-file nodes.json
```

This script:
- Checks if each node is accessible
- Verifies that the Sentry Node extension is running
- Attempts to restart nodes that are down
- Updates the node status in the nodes file
- Sends email alerts for persistent issues

### 2. Reward Collection

The `collect_rewards.py` script gathers reward data from the Gradient Network API:

```bash
python backend/scripts/collect_rewards.py --nodes-file nodes.json --db-file rewards.db --api-url https://api.gradient.network --api-key your-api-key
```

This script:
- Retrieves reward data for each node
- Stores the data in a SQLite database
- Calculates daily reward totals
- Tracks reward history over time

### 3. Data Analysis

The `analyze_data.py` script generates reports and insights from the collected data:

```bash
python backend/scripts/analyze_data.py --nodes-file nodes.json --db-file rewards.db --output-dir reports
```

This script:
- Analyzes rewards by node, day, and type
- Generates performance reports for each node
- Creates visualizations of reward trends
- Identifies optimization opportunities

### 4. Scheduled Tasks

The monitoring components are scheduled to run automatically:

- Node monitoring: Every 5 minutes
- POC taps: Every 12 hours
- Reward collection: Daily at midnight
- Data analysis: Daily at 1 AM

To set up these scheduled tasks:

```bash
./deploy.sh tasks
```

## Monitoring Dashboard

The monitoring dashboard provides a visual overview of your Sentry Nodes:

1. **Node Status** - Shows the current status of each node
2. **Reward Summary** - Displays total rewards and breakdown by type
3. **Performance Metrics** - Shows uptime, POC success rate, and reward rate
4. **Trend Analysis** - Visualizes reward trends over time

To access the dashboard:

1. Deploy the frontend to GitHub Pages:
   ```bash
   ./deploy.sh frontend
   ```

2. Open the dashboard in your browser:
   ```
   https://gemdeveng.github.io/GradientLab
   ```

## Optimization Strategies

Based on monitoring data, you can implement the following optimization strategies:

### 1. VM Distribution

Distribute your VMs across:
- **Multiple cloud providers** - Diversifies IP ranges
- **Different regions** - Improves geographic coverage
- **Various VM types** - Balances resource usage

### 2. POC Tap Timing

Optimize POC tap timing:
- **Schedule during peak hours** - When the network is most active
- **Stagger across nodes** - Avoid all nodes tapping at once
- **Adjust frequency** - Based on success rate and rewards

### 3. Resource Allocation

Allocate resources efficiently:
- **CPU priority** - Give Chromium higher CPU priority
- **Memory management** - Limit other processes to free up memory
- **Disk space** - Clean up logs and temporary files regularly

### 4. IP Rotation

Implement IP rotation strategies:
- **VPN integration** - Use VPNs to rotate IPs
- **Proxy services** - Route traffic through proxies
- **Cloud provider rotation** - Switch between providers periodically

## Performance Metrics

Track the following performance metrics:

1. **Uptime** - Percentage of time the node is online
2. **POC Success Rate** - Percentage of successful POC taps
3. **Reward Rate** - Average rewards per day
4. **Resource Usage** - CPU, memory, and disk usage

## Optimization Process

Follow this process to optimize your Sentry Nodes:

1. **Collect Data** - Gather performance data for at least a week
2. **Analyze Patterns** - Identify trends and correlations
3. **Implement Changes** - Make one change at a time
4. **Measure Impact** - Monitor the effect of each change
5. **Iterate** - Continuously refine your approach

## Alert Configuration

Configure alerts to notify you of issues:

1. Update the `tasks_config.json` file with your email settings:
   ```json
   {
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

2. Set up the scheduled tasks:
   ```bash
   ./deploy.sh tasks
   ```

## Troubleshooting

### Low Rewards

If a node is earning low rewards:

1. Check the node's uptime and connectivity
2. Verify that POC taps are successful
3. Check if the IP address is being rate-limited
4. Try rotating the IP address

### High Resource Usage

If a node is using too many resources:

1. Check for runaway processes
2. Restart the Chromium service
3. Reduce the number of browser tabs/instances
4. Increase the VM size if possible

### Frequent Downtime

If a node experiences frequent downtime:

1. Check the VM's stability in the cloud provider console
2. Verify network connectivity
3. Check for resource constraints
4. Consider moving to a different VM type or provider

## Next Steps

After setting up monitoring and optimization:

1. [Analyze reward data](../data_analysis/README.md)
2. [Implement advanced strategies](../advanced_strategies/README.md)
3. [Scale your Sentry Node operation](../scaling/README.md)
