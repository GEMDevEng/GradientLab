# Deploying GradientLab Backend to Heroku

This guide provides step-by-step instructions for deploying the GradientLab backend to Heroku.

## Prerequisites

1. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
2. Heroku account
3. Git installed

## Deployment Steps

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

### 5. Deploy the Backend

Navigate to the backend directory:

```bash
cd backend
```

Initialize a Git repository (if not already done):

```bash
git init
```

Add Heroku remote:

```bash
heroku git:remote -a gradientlab-api
```

Add and commit files:

```bash
git add .
git commit -m "Deploy backend to Heroku"
```

Push to Heroku:

```bash
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
git add .
git commit -m "Update backend"
git push heroku master
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

## Monitoring

Heroku provides basic monitoring through the dashboard. For more advanced monitoring, consider adding the New Relic add-on:

```bash
heroku addons:create newrelic:wayne --app gradientlab-api
```

## Backup

To backup the database:

```bash
heroku pg:backups:capture --app gradientlab-api
```

To download the backup:

```bash
heroku pg:backups:download --app gradientlab-api
```
