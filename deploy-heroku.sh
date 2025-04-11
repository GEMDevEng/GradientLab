#!/bin/bash

# GradientLab Heroku Deployment Script
# This script deploys the backend to Heroku

echo "Starting GradientLab backend deployment to Heroku..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI is not installed. Please install it first."
    echo "Visit https://devcenter.heroku.com/articles/heroku-cli for installation instructions."
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "You are not logged in to Heroku. Please login first."
    heroku login
fi

# Create Heroku app if it doesn't exist
if ! heroku apps:info gradientlab-api &> /dev/null; then
    echo "Creating Heroku app 'gradientlab-api'..."
    heroku create gradientlab-api
else
    echo "Heroku app 'gradientlab-api' already exists."
fi

# Add PostgreSQL add-on if it doesn't exist
if ! heroku addons:info --app gradientlab-api heroku-postgresql &> /dev/null; then
    echo "Adding PostgreSQL add-on..."
    heroku addons:create --app gradientlab-api heroku-postgresql:hobby-dev
else
    echo "PostgreSQL add-on already exists."
fi

# Set environment variables
echo "Setting environment variables..."
heroku config:set --app gradientlab-api FLASK_ENV=production
heroku config:set --app gradientlab-api FLASK_DEBUG=False

# Deploy backend to Heroku
echo "Deploying backend to Heroku..."
cd backend
git init
git add .
git commit -m "Deploy backend to Heroku"
git push --force heroku main

# Open the app in browser
echo "Opening app in browser..."
heroku open --app gradientlab-api

echo "Backend deployment to Heroku complete!"
