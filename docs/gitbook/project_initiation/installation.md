# Installation Guide

This guide provides step-by-step instructions for installing and setting up the GradientLab project.

## Prerequisites

Before installing GradientLab, ensure you have the following:

1. **Git**: For cloning the repository
2. **Python 3.9+**: For running the backend
3. **Node.js 16.x+**: For running the frontend
4. **Heroku CLI**: For deploying the backend (optional)
5. **Cloud Provider Accounts**: For deploying VMs (optional)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/GEMDevEng/GradientLab.git
cd GradientLab
```

### 2. Set Up the Backend

#### Create a Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Initialize the Database

```bash
python -c "from app import initialize_database; initialize_database()"
```

#### Run the Backend

```bash
python app.py
```

The backend will be available at http://localhost:5000.

### 3. Set Up the Frontend

#### Install Dependencies

```bash
cd ../frontend
npm install
```

#### Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Run the Frontend

```bash
npm start
```

The frontend will be available at http://localhost:3000.

## Production Deployment

### 1. Deploy the Backend to Heroku

#### Log in to Heroku

```bash
heroku login
```

#### Create a Heroku App

```bash
cd backend
heroku create gradientlab-api
```

#### Add PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:hobby-dev --app gradientlab-api
```

#### Set Environment Variables

```bash
heroku config:set FLASK_ENV=production --app gradientlab-api
heroku config:set FLASK_DEBUG=False --app gradientlab-api
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32) --app gradientlab-api
```

#### Deploy the Backend

```bash
git subtree push --prefix backend heroku master
```

#### Initialize the Database

```bash
heroku run python -c "from app import initialize_database; initialize_database()" --app gradientlab-api
```

### 2. Deploy the Frontend to GitHub Pages

#### Set Up GitHub Pages

```bash
cd ../frontend
```

Edit `package.json` to add:

```json
"homepage": "https://gemdeveng.github.io/GradientLab",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```

#### Install gh-pages

```bash
npm install --save-dev gh-pages
```

#### Deploy to GitHub Pages

```bash
npm run deploy
```

### 3. Automated Deployment

For automated deployment, use the provided script:

```bash
./deploy.sh all
```

This script will:
1. Deploy the backend to Heroku
2. Deploy the frontend to GitHub Pages
3. Provision VMs on cloud providers (if configured)
4. Set up scheduled tasks (if configured)

## VM Provisioning

### 1. Set Up Cloud Provider Accounts

Follow the guides in the [Cloud Setup](../guides/cloud_setup/README.md) section to set up accounts with:
- Oracle Cloud
- Google Cloud
- Azure

### 2. Configure VM Provisioning

Edit the `vm_config.json` file with your cloud provider details:

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

### 3. Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -f gradient_ssh_key -N ""
```

### 4. Provision VMs

```bash
./deploy.sh vms
```

## Scheduled Tasks

### 1. Configure Scheduled Tasks

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

### 2. Set Up Scheduled Tasks

```bash
./deploy.sh tasks
```

## Verification

### 1. Verify Backend Deployment

```bash
curl https://gradientlab-api.herokuapp.com/api/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Verify Frontend Deployment

Open https://gemdeveng.github.io/GradientLab in your browser.

### 3. Verify VM Provisioning

```bash
python backend/scripts/monitor_nodes.py --nodes-file nodes.json
```

### 4. Verify Scheduled Tasks

```bash
crontab -l
```

## Troubleshooting

### Backend Issues

- **Database Connection Error**: Check the `DATABASE_URL` environment variable
- **API Key Error**: Verify the Gradient Network API key
- **Port Already in Use**: Change the port in the `.env` file

### Frontend Issues

- **API Connection Error**: Check the `REACT_APP_API_URL` environment variable
- **Build Error**: Check for syntax errors in the code
- **Deployment Error**: Verify GitHub Pages configuration

### VM Issues

- **Provisioning Error**: Check cloud provider credentials
- **SSH Connection Error**: Verify SSH key configuration
- **Node Installation Error**: Check the installation logs

### Scheduled Task Issues

- **Cron Job Error**: Check crontab syntax
- **Script Execution Error**: Verify script permissions
- **Email Alert Error**: Check SMTP configuration

## Next Steps

After installation, proceed to:

1. [User Guide](../guides/user_guide/README.md): Learn how to use GradientLab
2. [Admin Guide](../guides/admin_guide/README.md): Learn how to administer GradientLab
3. [Developer Guide](../guides/developer_guide/README.md): Learn how to extend GradientLab
