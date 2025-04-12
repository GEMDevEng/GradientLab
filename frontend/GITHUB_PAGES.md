# Deploying GradientLab Frontend to GitHub Pages

This guide provides detailed instructions for deploying the GradientLab frontend to GitHub Pages.

## Prerequisites

1. Node.js and npm installed
2. Git installed
3. GitHub account with access to the repository

## Manual Deployment Steps

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure GitHub Pages

Make sure your package.json has the following:

```json
{
  "homepage": "https://gemdeveng.github.io/GradientLab",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  },
  "devDependencies": {
    "gh-pages": "^3.2.3"
  }
}
```

### 3. Build and Deploy

```bash
npm run deploy
```

This will:
1. Build the React application
2. Create a gh-pages branch if it doesn't exist
3. Push the build files to the gh-pages branch

### 4. Verify Deployment

After a few minutes, your site should be available at:
https://gemdeveng.github.io/GradientLab

## Automated Deployment

For automated deployment, use the provided script:

```bash
./deploy-gh-pages.sh
```

This script will:
1. Install the gh-pages package if needed
2. Install dependencies
3. Build the app
4. Deploy to GitHub Pages

## Troubleshooting

### 404 Error

If you get a 404 error when accessing your site:

1. Check if the gh-pages branch exists in your repository
2. Make sure the "homepage" in package.json matches your GitHub Pages URL
3. Check if GitHub Pages is enabled in your repository settings

### Build Errors

If you encounter build errors:

1. Check your dependencies
2. Make sure your code is compatible with the build process
3. Check for any environment variables that need to be set

### Deployment Errors

If you encounter deployment errors:

1. Make sure you have write access to the repository
2. Check if your SSH key is set up correctly
3. Try running the deployment with verbose logging:
   ```bash
   GIT_TRACE=1 npm run deploy
   ```

## Custom Domain (Optional)

To use a custom domain:

1. Add your domain in the GitHub repository settings under "GitHub Pages"
2. Create a CNAME file in the public directory with your domain:
   ```
   echo "yourdomain.com" > public/CNAME
   ```
3. Update the "homepage" in package.json to match your custom domain:
   ```json
   "homepage": "https://yourdomain.com"
   ```
4. Deploy again

## Updating the Deployment

To update the deployment after making changes:

```bash
npm run deploy
```

Or use the deployment script:

```bash
./deploy-gh-pages.sh
```
