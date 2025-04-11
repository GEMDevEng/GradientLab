#!/bin/bash

# GradientLab Deployment Script
# This script builds and deploys the GradientLab application to GitHub Pages

echo "Starting GradientLab deployment..."

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
