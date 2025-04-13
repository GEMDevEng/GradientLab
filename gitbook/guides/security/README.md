# Security Guide for GradientLab

This guide provides comprehensive security recommendations and best practices for securing your GradientLab deployment and Gradient Sentry Nodes.

## Security Overview

Security is critical for GradientLab for several reasons:

1. **Protecting Rewards** - Securing your nodes and accounts to protect earned rewards
2. **Preventing Unauthorized Access** - Ensuring only authorized users can access your nodes
3. **Maintaining Node Integrity** - Preventing tampering with node operations
4. **Protecting Sensitive Data** - Securing API keys, credentials, and personal information

## Security Layers

GradientLab security is implemented in multiple layers:

### 1. Cloud Provider Security

Secure your cloud provider accounts:

- **Strong Passwords** - Use strong, unique passwords for all cloud accounts
- **Multi-Factor Authentication (MFA)** - Enable MFA for all cloud provider accounts
- **Limited Permissions** - Use the principle of least privilege for service accounts
- **Regular Audits** - Regularly audit access logs and permissions

### 2. VM Security

Secure your virtual machines:

- **SSH Key Authentication** - Use SSH keys instead of passwords
- **Firewall Configuration** - Restrict inbound traffic to necessary ports only
- **Regular Updates** - Keep the OS and software up to date
- **Minimal Services** - Run only necessary services on each VM

### 3. Application Security

Secure the GradientLab application:

- **API Key Protection** - Securely store and manage API keys
- **Secure Configuration** - Protect configuration files with sensitive information
- **Input Validation** - Validate all input to prevent injection attacks
- **Output Encoding** - Properly encode output to prevent XSS attacks

### 4. Network Security

Secure network communications:

- **HTTPS** - Use HTTPS for all web traffic
- **VPN/Proxy** - Use VPNs or proxies for additional IP security
- **Network Segmentation** - Isolate different components of your infrastructure
- **Traffic Monitoring** - Monitor network traffic for suspicious activity

## Security Hardening Steps

Follow these steps to harden your GradientLab deployment:

### 1. Secure Cloud Accounts

For each cloud provider:

1. **Enable MFA**
   ```
   # Oracle Cloud
   Profile > My Profile > Multi-Factor Authentication > Enable

   # Google Cloud
   Security > 2-Step Verification > Get Started

   # Azure
   Security Info > Add Method > Authenticator App
   ```

2. **Create Dedicated Service Accounts**
   - Create separate accounts for automation with minimal permissions
   - Regularly rotate service account credentials

3. **Enable Audit Logging**
   - Enable detailed audit logging for all actions
   - Set up alerts for suspicious activities

### 2. Secure VMs

For each VM:

1. **Update the System**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt upgrade -y

   # Oracle Linux/RHEL
   sudo yum update -y
   ```

2. **Configure Firewall**
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable

   # Oracle Linux/RHEL
   sudo firewall-cmd --permanent --add-service=ssh
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   sudo firewall-cmd --reload
   ```

3. **Secure SSH**
   ```bash
   # Edit SSH config
   sudo nano /etc/ssh/sshd_config

   # Set these options
   PermitRootLogin no
   PasswordAuthentication no
   PubkeyAuthentication yes
   
   # Restart SSH
   sudo systemctl restart sshd
   ```

4. **Install Security Updates Automatically**
   ```bash
   # Ubuntu/Debian
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades

   # Oracle Linux/RHEL
   sudo yum install yum-cron
   sudo systemctl enable yum-cron
   sudo systemctl start yum-cron
   ```

### 3. Secure Application

For the GradientLab application:

1. **Protect API Keys**
   - Store API keys in environment variables, not in code
   - Use a .env file that is not committed to version control

2. **Secure Configuration Files**
   ```bash
   # Set proper permissions
   chmod 600 vm_config.json
   chmod 600 tasks_config.json
   chmod 600 gradient_ssh_key
   ```

3. **Encrypt Sensitive Data**
   ```bash
   # Encrypt configuration files when not in use
   gpg --symmetric --cipher-algo AES256 vm_config.json
   ```

4. **Use HTTPS for API Communication**
   - Update API URLs to use HTTPS
   - Verify SSL certificates

### 4. Implement Network Security

For network communications:

1. **Set Up a VPN**
   ```bash
   # Install OpenVPN
   sudo apt install openvpn

   # Configure OpenVPN client
   sudo cp client.ovpn /etc/openvpn/
   sudo systemctl enable openvpn@client
   sudo systemctl start openvpn@client
   ```

2. **Use a Proxy for Outbound Traffic**
   ```bash
   # Install Squid proxy
   sudo apt install squid

   # Configure Chromium to use the proxy
   export HTTP_PROXY=http://localhost:3128
   export HTTPS_PROXY=http://localhost:3128
   ```

3. **Implement IP Rotation**
   - Set up scheduled IP rotation using VPNs or proxies
   - Distribute nodes across different providers and regions

## Security Monitoring

Implement monitoring to detect security issues:

### 1. System Monitoring

Monitor system security:

- **Log Monitoring**
  ```bash
  # Install fail2ban to monitor and block suspicious activity
  sudo apt install fail2ban
  sudo systemctl enable fail2ban
  sudo systemctl start fail2ban
  ```

- **Intrusion Detection**
  ```bash
  # Install OSSEC
  wget https://github.com/ossec/ossec-hids/archive/3.6.0.tar.gz
  tar -xzf 3.6.0.tar.gz
  cd ossec-hids-3.6.0
  ./install.sh
  ```

- **File Integrity Monitoring**
  ```bash
  # Monitor critical files for changes
  sudo apt install aide
  sudo aideinit
  sudo cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db
  ```

### 2. Network Monitoring

Monitor network security:

- **Traffic Analysis**
  ```bash
  # Install tcpdump
  sudo apt install tcpdump

  # Monitor suspicious traffic
  sudo tcpdump -i eth0 -n "not port 22"
  ```

- **Port Scanning Detection**
  ```bash
  # Install psad
  sudo apt install psad
  sudo systemctl enable psad
  sudo systemctl start psad
  ```

### 3. Application Monitoring

Monitor application security:

- **API Usage Monitoring**
  - Track API calls and look for unusual patterns
  - Set up alerts for excessive API usage

- **Authentication Monitoring**
  - Monitor login attempts and failures
  - Alert on suspicious authentication activities

## Security Incident Response

Prepare for security incidents:

### 1. Incident Response Plan

Create a plan for responding to security incidents:

1. **Detection** - Identify the security incident
2. **Containment** - Isolate affected systems
3. **Eradication** - Remove the threat
4. **Recovery** - Restore systems to normal operation
5. **Lessons Learned** - Analyze the incident and improve security

### 2. Backup and Recovery

Implement backup and recovery procedures:

- **Regular Backups**
  ```bash
  # Backup configuration files
  rsync -avz --delete /path/to/config/ /path/to/backup/

  # Backup database
  sqlite3 rewards.db .dump > rewards_backup.sql
  ```

- **Disaster Recovery**
  - Document steps to recover from various scenarios
  - Test recovery procedures regularly

## Next Steps

After implementing security enhancements:

1. [Conduct a security audit](security_audit.md)
2. [Set up continuous security monitoring](security_monitoring.md)
3. [Develop an incident response plan](incident_response.md)
