from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
import os
import logging
from datetime import timedelta
from dotenv import load_dotenv
from middleware.security import HTTPSRedirect, RateLimiter

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database configuration
from config.database import init_db

# Import models
from models.user import create_admin_user

# Import API blueprints
from api.vm_provision import vm_provision_bp
from api.node_deploy import node_deploy_bp
from api.data_collect import data_collect_bp
from api.referral_manage import referral_manage_bp
from api.auth import auth_bp
from api.realtime import realtime_bp
from api.two_factor import two_factor_bp

# Import WebSocket
from websocket.socket_manager import init_app as init_socketio

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Configure security
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['WTF_CSRF_ENABLED'] = os.environ.get('FLASK_ENV', 'production') != 'development'
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour
app.config['WTF_CSRF_SSL_STRICT'] = True

# Initialize security extensions
jwt = JWTManager(app)
csrf = CSRFProtect(app)

# Enable CORS for all routes
cors = CORS(app, supports_credentials=True)

# Apply security middleware
if os.environ.get('FLASK_ENV', 'production') != 'development':
    app.wsgi_app = HTTPSRedirect(app.wsgi_app)
    app.wsgi_app = RateLimiter(app.wsgi_app, limit=100, window=60)

# Register API blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(vm_provision_bp, url_prefix='/api/vm')
app.register_blueprint(node_deploy_bp, url_prefix='/api/node')
app.register_blueprint(data_collect_bp, url_prefix='/api/data')
app.register_blueprint(referral_manage_bp, url_prefix='/api/referral')
app.register_blueprint(realtime_bp, url_prefix='/api/realtime')
app.register_blueprint(two_factor_bp, url_prefix='/api/2fa')

# Initialize WebSocket
socketio = init_socketio(app)
logger.info("WebSocket initialized")

@app.route('/')
def index():
    """Root endpoint for the API."""
    return jsonify({
        'message': 'Welcome to GradientLab API',
        'status': 'online',
        'version': '0.1.0',
        'endpoints': [
            '/api/vm/vms',
            '/api/vm/providers',
            '/api/node/nodes',
            '/api/data/rewards',
            '/api/data/rewards/stats',
            '/api/referral/referrals'
        ]
    })

@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy'
    })

# Initialize database
@app.before_first_request
def initialize_database():
    """Initialize the database before the first request."""
    try:
        # Initialize database tables
        init_db()

        # Create default admin user
        create_admin_user()

        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

if __name__ == '__main__':
    # Initialize database
    init_db()
    create_admin_user()

    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    # Run the app with WebSocket support
    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
