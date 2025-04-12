#!/bin/bash
# Script to deploy the frontend to GitHub Pages

# Exit on error
set -e

# Log file
LOG_FILE="deploy-gh-pages.log"

# Function to log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Create log file
touch $LOG_FILE
chmod 644 $LOG_FILE

log "Starting deployment to GitHub Pages"

# Check if gh-pages package is installed
if ! npm list -g gh-pages > /dev/null 2>&1; then
    log "Installing gh-pages package"
    npm install -g gh-pages
fi

# Install dependencies
log "Installing dependencies"
npm install

# Build the app
log "Building the app"
npm run build

# Deploy to GitHub Pages
log "Deploying to GitHub Pages"
gh-pages -d build

log "Deployment completed successfully"
