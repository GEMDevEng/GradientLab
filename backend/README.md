# GradientLab Backend

This is the backend for the GradientLab application, a web app to automate VM setup and Sentry Node management on the Gradient Network.

## Deployment to Heroku

### Prerequisites

1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku: `heroku login`

### Deployment Steps

1. Create a new Heroku app:
   ```
   heroku create gradientlab-api
   ```

2. Add PostgreSQL add-on:
   ```
   heroku addons:create heroku-postgresql:hobby-dev --app gradientlab-api
   ```

3. Set environment variables:
   ```
   heroku config:set FLASK_ENV=production --app gradientlab-api
   heroku config:set FLASK_DEBUG=False --app gradientlab-api
   heroku config:set JWT_SECRET_KEY=$(openssl rand -hex 32) --app gradientlab-api
   ```

4. Deploy the backend:
   ```
   cd backend
   git init
   heroku git:remote -a gradientlab-api
   git add .
   git commit -m "Deploy backend to Heroku"
   git push heroku master
   ```

5. Initialize the database:
   ```
   heroku run python -c "from app import initialize_database; initialize_database()" --app gradientlab-api
   ```

6. Open the app:
   ```
   heroku open --app gradientlab-api
   ```

## API Endpoints

### Authentication

- `POST /api/auth/register`: Register a new user
- `POST /api/auth/login`: Login a user
- `GET /api/auth/user`: Get current user information

### VM Provisioning

- `POST /api/vm/provision`: Provision a new VM
- `GET /api/vm/list`: Get list of VMs
- `GET /api/vm/{id}`: Get VM details
- `DELETE /api/vm/{id}`: Delete a VM

### Node Deployment

- `POST /api/node/deploy`: Deploy a Sentry Node
- `GET /api/node/list`: Get list of nodes
- `GET /api/node/{id}`: Get node details
- `DELETE /api/node/{id}`: Delete a node

### Data Collection

- `GET /api/data/rewards`: Get reward data
- `GET /api/data/stats`: Get statistics

### Referral Management

- `POST /api/referral/generate`: Generate a referral link
- `GET /api/referral/list`: Get list of referrals

### Real-time Updates

- `GET /api/realtime/status`: Get real-time status

### Two-Factor Authentication

- `POST /api/2fa/setup`: Set up two-factor authentication
- `GET /api/2fa/qrcode`: Get QR code for two-factor authentication
- `POST /api/2fa/verify`: Verify two-factor authentication code
- `POST /api/2fa/disable`: Disable two-factor authentication
- `GET /api/2fa/backup-codes`: Get backup codes
- `POST /api/2fa/backup-codes/regenerate`: Regenerate backup codes
- `GET /api/2fa/status`: Get two-factor authentication status

## Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export DATABASE_URL=sqlite:///gradientlab.db
   ```

4. Run the application:
   ```
   flask run
   ```

5. For WebSocket support:
   ```
   python app.py
   ```
