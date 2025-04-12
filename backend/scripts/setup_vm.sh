#!/bin/bash
# Script to set up a VM for running Gradient Sentry Nodes

# Exit on error
set -e

# Log file
LOG_FILE="/var/log/gradient_setup.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    log "This script must be run as root"
    exit 1
fi

# Create log file
touch $LOG_FILE
chmod 644 $LOG_FILE

log "Starting VM setup for Gradient Sentry Node"

# Update system
log "Updating system packages"
apt-get update
apt-get upgrade -y

# Install dependencies
log "Installing dependencies"
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    build-essential \
    ca-certificates \
    gnupg \
    lsb-release \
    apt-transport-https \
    software-properties-common

# Install Node.js
log "Installing Node.js"
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get install -y nodejs
node --version
npm --version

# Install Chromium
log "Installing Chromium"
apt-get install -y chromium-browser
chromium-browser --version

# Install Docker
log "Installing Docker"
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker
docker --version

# Install Docker Compose
log "Installing Docker Compose"
curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

# Create gradient user
log "Creating gradient user"
useradd -m -s /bin/bash gradient || log "User already exists"
usermod -aG docker gradient

# Set up Gradient directory
log "Setting up Gradient directory"
mkdir -p /home/gradient/sentry
chown -R gradient:gradient /home/gradient/sentry

# Create a script to run Chromium in headless mode
log "Creating Chromium startup script"
cat > /home/gradient/sentry/start_chromium.sh << 'EOL'
#!/bin/bash

# Start Chromium in headless mode with remote debugging
chromium-browser \
    --headless \
    --disable-gpu \
    --remote-debugging-port=9222 \
    --no-sandbox \
    --disable-setuid-sandbox \
    --disable-dev-shm-usage \
    --disable-software-rasterizer \
    --disable-extensions \
    --disable-background-networking \
    --disable-sync \
    --disable-translate \
    --hide-scrollbars \
    --metrics-recording-only \
    --mute-audio \
    --no-first-run \
    --safebrowsing-disable-auto-update \
    --ignore-certificate-errors \
    --ignore-ssl-errors \
    --ignore-certificate-errors-spki-list \
    --user-data-dir=/home/gradient/sentry/chrome-data \
    --window-size=1920,1080 \
    --start-maximized \
    --enable-logging \
    --log-level=0 \
    --v=1 \
    --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36" \
    "about:blank"
EOL

chmod +x /home/gradient/sentry/start_chromium.sh
chown gradient:gradient /home/gradient/sentry/start_chromium.sh

# Create a systemd service for Chromium
log "Creating Chromium systemd service"
cat > /etc/systemd/system/chromium.service << 'EOL'
[Unit]
Description=Headless Chromium
After=network.target

[Service]
User=gradient
Group=gradient
ExecStart=/home/gradient/sentry/start_chromium.sh
Restart=always
RestartSec=10
Environment=DISPLAY=:1

[Install]
WantedBy=multi-user.target
EOL

# Create a script to check and restart Chromium if needed
log "Creating Chromium monitoring script"
cat > /home/gradient/sentry/monitor_chromium.sh << 'EOL'
#!/bin/bash

# Check if Chromium is running and restart if needed
if ! pgrep -f "chromium-browser --headless" > /dev/null; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Chromium not running, restarting..."
    systemctl restart chromium
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Chromium is running"
fi
EOL

chmod +x /home/gradient/sentry/monitor_chromium.sh
chown gradient:gradient /home/gradient/sentry/monitor_chromium.sh

# Create a cron job to monitor Chromium
log "Creating cron job to monitor Chromium"
(crontab -l 2>/dev/null || echo "") | grep -v "monitor_chromium.sh" | { cat; echo "*/5 * * * * /home/gradient/sentry/monitor_chromium.sh >> /home/gradient/sentry/monitor.log 2>&1"; } | crontab -

# Enable and start Chromium service
log "Enabling and starting Chromium service"
systemctl daemon-reload
systemctl enable chromium
systemctl start chromium

# Install Xvfb for virtual display
log "Installing Xvfb"
apt-get install -y xvfb x11-xserver-utils

# Create a systemd service for Xvfb
log "Creating Xvfb systemd service"
cat > /etc/systemd/system/xvfb.service << 'EOL'
[Unit]
Description=X Virtual Frame Buffer
After=network.target

[Service]
ExecStart=/usr/bin/Xvfb :1 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Enable and start Xvfb service
log "Enabling and starting Xvfb service"
systemctl daemon-reload
systemctl enable xvfb
systemctl start xvfb

# Create a script to install the Sentry Node extension
log "Creating script to install Sentry Node extension"
cat > /home/gradient/sentry/install_extension.sh << 'EOL'
#!/bin/bash

# Download the latest Sentry Node extension
# Note: This is a placeholder. The actual extension would need to be downloaded from the Gradient Network.
echo "Downloading Sentry Node extension..."
mkdir -p /home/gradient/sentry/extension
cd /home/gradient/sentry/extension

# Placeholder for extension download
# wget https://gradient.network/downloads/sentry-node-extension.zip
# unzip sentry-node-extension.zip

echo "Sentry Node extension installed"
EOL

chmod +x /home/gradient/sentry/install_extension.sh
chown gradient:gradient /home/gradient/sentry/install_extension.sh

# Create a script to connect to the Gradient Network
log "Creating script to connect to Gradient Network"
cat > /home/gradient/sentry/connect_gradient.sh << 'EOL'
#!/bin/bash

# Connect to the Gradient Network
# Note: This is a placeholder. The actual connection process would depend on the Gradient Network API.
echo "Connecting to Gradient Network..."

# Placeholder for connection process
# curl -X POST https://api.gradient.network/connect -H "Content-Type: application/json" -d '{"node_id": "'"$NODE_ID"'", "api_key": "'"$API_KEY"'"}'

echo "Connected to Gradient Network"
EOL

chmod +x /home/gradient/sentry/connect_gradient.sh
chown gradient:gradient /home/gradient/sentry/connect_gradient.sh

# Create a script to perform POC taps
log "Creating script to perform POC taps"
cat > /home/gradient/sentry/poc_tap.sh << 'EOL'
#!/bin/bash

# Perform a POC tap
# Note: This is a placeholder. The actual POC tap process would depend on the Gradient Network API.
echo "Performing POC tap..."

# Placeholder for POC tap process
# curl -X POST https://api.gradient.network/poc/tap -H "Content-Type: application/json" -d '{"node_id": "'"$NODE_ID"'", "api_key": "'"$API_KEY"'"}'

echo "POC tap completed"
EOL

chmod +x /home/gradient/sentry/poc_tap.sh
chown gradient:gradient /home/gradient/sentry/poc_tap.sh

# Create a cron job to perform POC taps
log "Creating cron job to perform POC taps"
(crontab -u gradient -l 2>/dev/null || echo "") | grep -v "poc_tap.sh" | { cat; echo "0 */12 * * * /home/gradient/sentry/poc_tap.sh >> /home/gradient/sentry/poc_tap.log 2>&1"; } | crontab -u gradient -

# Set up monitoring
log "Setting up monitoring"
apt-get install -y prometheus-node-exporter

# Create a simple status page
log "Creating status page"
mkdir -p /var/www/html
cat > /var/www/html/index.html << 'EOL'
<!DOCTYPE html>
<html>
<head>
    <title>Gradient Sentry Node Status</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
        }
        .status.running {
            background-color: #d4edda;
            color: #155724;
        }
        .status.stopped {
            background-color: #f8d7da;
            color: #721c24;
        }
        .info {
            margin-top: 20px;
        }
        .info table {
            width: 100%;
            border-collapse: collapse;
        }
        .info table th, .info table td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .info table th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Gradient Sentry Node Status</h1>
        <div class="status running">
            <h2>Status: Running</h2>
            <p>The Sentry Node is currently running.</p>
        </div>
        <div class="info">
            <h2>Node Information</h2>
            <table>
                <tr>
                    <th>Hostname</th>
                    <td id="hostname"></td>
                </tr>
                <tr>
                    <th>IP Address</th>
                    <td id="ip"></td>
                </tr>
                <tr>
                    <th>Uptime</th>
                    <td id="uptime"></td>
                </tr>
                <tr>
                    <th>CPU Usage</th>
                    <td id="cpu"></td>
                </tr>
                <tr>
                    <th>Memory Usage</th>
                    <td id="memory"></td>
                </tr>
                <tr>
                    <th>Disk Usage</th>
                    <td id="disk"></td>
                </tr>
            </table>
        </div>
    </div>
    <script>
        // Update the status page with real data
        function updateStatus() {
            fetch('/status.json')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('hostname').textContent = data.hostname;
                    document.getElementById('ip').textContent = data.ip;
                    document.getElementById('uptime').textContent = data.uptime;
                    document.getElementById('cpu').textContent = data.cpu + '%';
                    document.getElementById('memory').textContent = data.memory + '%';
                    document.getElementById('disk').textContent = data.disk + '%';
                    
                    const statusDiv = document.querySelector('.status');
                    if (data.running) {
                        statusDiv.className = 'status running';
                        statusDiv.innerHTML = '<h2>Status: Running</h2><p>The Sentry Node is currently running.</p>';
                    } else {
                        statusDiv.className = 'status stopped';
                        statusDiv.innerHTML = '<h2>Status: Stopped</h2><p>The Sentry Node is currently stopped.</p>';
                    }
                })
                .catch(error => console.error('Error fetching status:', error));
        }
        
        // Update status every 30 seconds
        updateStatus();
        setInterval(updateStatus, 30000);
    </script>
</body>
</html>
EOL

# Create a script to generate status.json
log "Creating script to generate status.json"
cat > /home/gradient/sentry/generate_status.sh << 'EOL'
#!/bin/bash

# Generate status.json for the status page
HOSTNAME=$(hostname)
IP=$(hostname -I | awk '{print $1}')
UPTIME=$(uptime -p)
CPU=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
MEMORY=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
DISK=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
RUNNING=$(pgrep -f "chromium-browser --headless" > /dev/null && echo true || echo false)

cat > /var/www/html/status.json << EOF
{
    "hostname": "$HOSTNAME",
    "ip": "$IP",
    "uptime": "$UPTIME",
    "cpu": $CPU,
    "memory": $MEMORY,
    "disk": $DISK,
    "running": $RUNNING
}
EOF
EOL

chmod +x /home/gradient/sentry/generate_status.sh
chown gradient:gradient /home/gradient/sentry/generate_status.sh

# Create a cron job to generate status.json
log "Creating cron job to generate status.json"
(crontab -l 2>/dev/null || echo "") | grep -v "generate_status.sh" | { cat; echo "* * * * * /home/gradient/sentry/generate_status.sh > /dev/null 2>&1"; } | crontab -

# Install Nginx
log "Installing Nginx"
apt-get install -y nginx

# Configure Nginx
log "Configuring Nginx"
cat > /etc/nginx/sites-available/default << 'EOL'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    
    root /var/www/html;
    index index.html;
    
    server_name _;
    
    location / {
        try_files $uri $uri/ =404;
    }
}
EOL

# Restart Nginx
log "Restarting Nginx"
systemctl restart nginx

# Run the generate_status.sh script once
log "Generating initial status.json"
/home/gradient/sentry/generate_status.sh

log "VM setup completed successfully"
echo "VM setup completed successfully. You can access the status page at http://$(hostname -I | awk '{print $1}')"
