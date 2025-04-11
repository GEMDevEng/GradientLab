#!/bin/bash

# GradientLab Deployment Script
# This script builds and deploys the GradientLab application to GitHub Pages and Heroku

echo "Starting GradientLab deployment..."

# Deploy backend to Heroku
echo "Deploying backend to Heroku..."
./deploy-heroku.sh

# Build the React frontend
echo "Building React frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy to GitHub Pages
echo "Deploying to GitHub Pages..."
cd frontend
npm run deploy
cd ..

echo "Deployment complete!"
echo "Frontend: https://gemdeveng.github.io/GradientLab"
echo "Backend: https://gradientlab-api.herokuapp.com"
