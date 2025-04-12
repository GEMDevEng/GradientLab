#!/bin/bash
# Script to deploy the backend to Heroku

# Exit on error
set -e

# Log file
LOG_FILE="deploy-heroku.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Create log file
touch $LOG_FILE
chmod 644 $LOG_FILE

log "Starting deployment to Heroku"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    log "Heroku CLI is not installed. Please install it first."
    exit 1
fi

# Check if logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    log "Not logged in to Heroku. Please run 'heroku login' first."
    exit 1
fi

# Get app name from command line or use default
APP_NAME=${1:-gradientlab-api}

# Check if app exists
if ! heroku apps:info --app $APP_NAME &> /dev/null; then
    log "Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
else
    log "Using existing Heroku app: $APP_NAME"
fi

# Check if PostgreSQL add-on is installed
if ! heroku addons:info --app $APP_NAME postgresql &> /dev/null; then
    log "Adding PostgreSQL add-on"
    heroku addons:create --app $APP_NAME heroku-postgresql:hobby-dev
else
    log "PostgreSQL add-on already installed"
fi

# Set environment variables
log "Setting environment variables"
heroku config:set --app $APP_NAME FLASK_ENV=production
heroku config:set --app $APP_NAME FLASK_DEBUG=False
heroku config:set --app $APP_NAME JWT_SECRET_KEY=$(openssl rand -hex 32)

# Deploy to Heroku
log "Deploying to Heroku"
git subtree push --prefix backend heroku master

# Initialize the database
log "Initializing the database"
heroku run --app $APP_NAME python -c "from app import initialize_database; initialize_database()"

log "Deployment completed successfully"
log "Your app is running at: https://$APP_NAME.herokuapp.com"
