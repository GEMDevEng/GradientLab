# Deploying GradientLab Backend to Heroku

This guide provides detailed instructions for deploying the GradientLab backend to Heroku.

## Prerequisites

1. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
2. Heroku account
3. Git installed

## Manual Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Create a Heroku App

```bash
heroku create gradientlab-api
```

Replace `gradientlab-api` with your preferred app name.

### 3. Add PostgreSQL Add-on

```bash
heroku addons:create heroku-postgresql:hobby-dev --app gradientlab-api
```

### 4. Set Environment Variables

```bash
heroku config:set FLASK_ENV=production --app gradientlab-api
heroku config:set FLASK_DEBUG=False --app gradientlab-api
heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32) --app gradientlab-api
```

Add any other environment variables needed for your application:

```bash
heroku config:set GRADIENT_API_KEY=your-api-key --app gradientlab-api
```

### 5. Deploy the Backend

Navigate to the root directory of the repository:

```bash
git subtree push --prefix backend heroku master
```

Alternatively, if you're in the backend directory:

```bash
git init
heroku git:remote -a gradientlab-api
git add .
git commit -m "Deploy backend to Heroku"
git push heroku master
```

### 6. Initialize the Database

```bash
heroku run python -c "from app import initialize_database; initialize_database()" --app gradientlab-api
```

### 7. Verify Deployment

```bash
heroku open --app gradientlab-api
```

This should open the backend API in your browser. You should see a JSON response with a "status" field set to "healthy".

## Automated Deployment

For automated deployment, use the provided script:

```bash
./deploy-heroku.sh gradientlab-api
```

This script will:
1. Check if Heroku CLI is installed and you're logged in
2. Create a Heroku app if it doesn't exist
3. Add PostgreSQL add-on if it's not already added
4. Set environment variables
5. Deploy the backend
6. Initialize the database

## Troubleshooting

### View Logs

```bash
heroku logs --tail --app gradientlab-api
```

### Restart the App

```bash
heroku restart --app gradientlab-api
```

### Check Configuration

```bash
heroku config --app gradientlab-api
```

### Connect to PostgreSQL Database

```bash
heroku pg:psql --app gradientlab-api
```

## Updating the Deployment

To update the deployment after making changes:

```bash
git subtree push --prefix backend heroku master
```

Or use the deployment script:

```bash
./deploy-heroku.sh gradientlab-api
```

## Scaling

To scale the app:

```bash
heroku ps:scale web=1 --app gradientlab-api
```

## Custom Domain (Optional)

To add a custom domain:

```bash
heroku domains:add api.yourdomain.com --app gradientlab-api
```

Follow the instructions to configure DNS settings.
