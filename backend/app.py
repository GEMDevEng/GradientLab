from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import API blueprints
from api.vm_provision import vm_provision_bp
from api.node_deploy import node_deploy_bp
from api.data_collect import data_collect_bp
from api.referral_manage import referral_manage_bp

# Create Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Register API blueprints
app.register_blueprint(vm_provision_bp, url_prefix='/api/vm')
app.register_blueprint(node_deploy_bp, url_prefix='/api/node')
app.register_blueprint(data_collect_bp, url_prefix='/api/data')
app.register_blueprint(referral_manage_bp, url_prefix='/api/referral')

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

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))

    # Run the app
    app.run(host='0.0.0.0', port=port, debug=True)
