"""
Security middleware for GradientLab backend.
"""
from flask import request, redirect
import os

class HTTPSRedirect:
    """Middleware to redirect HTTP requests to HTTPS."""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        """Process the request."""
        # Skip HTTPS redirect in development
        if os.environ.get('FLASK_ENV') == 'development':
            return self.app(environ, start_response)
        
        # Check if request is secure
        if environ.get('wsgi.url_scheme') == 'https':
            return self.app(environ, start_response)
        
        # Redirect to HTTPS
        url = request.url.replace('http://', 'https://', 1)
        response = redirect(url, code=301)
        return response(environ, start_response)

class RateLimiter:
    """Middleware to limit request rate."""
    
    def __init__(self, app, limit=100, window=60):
        self.app = app
        self.limit = limit  # Number of requests
        self.window = window  # Time window in seconds
        self.clients = {}
    
    def __call__(self, environ, start_response):
        """Process the request."""
        # Skip rate limiting in development
        if os.environ.get('FLASK_ENV') == 'development':
            return self.app(environ, start_response)
        
        # Get client IP
        client_ip = environ.get('REMOTE_ADDR')
        
        # Check if client is rate limited
        if self._is_rate_limited(client_ip):
            # Return 429 Too Many Requests
            response_headers = [('Content-Type', 'text/plain')]
            start_response('429 Too Many Requests', response_headers)
            return [b'Too many requests. Please try again later.']
        
        return self.app(environ, start_response)
    
    def _is_rate_limited(self, client_ip):
        """Check if client is rate limited."""
        from time import time
        
        # Get current time
        now = time()
        
        # Initialize client if not exists
        if client_ip not in self.clients:
            self.clients[client_ip] = {
                'requests': 0,
                'window_start': now
            }
        
        # Reset window if expired
        if now - self.clients[client_ip]['window_start'] > self.window:
            self.clients[client_ip]['requests'] = 0
            self.clients[client_ip]['window_start'] = now
        
        # Increment request count
        self.clients[client_ip]['requests'] += 1
        
        # Check if rate limited
        return self.clients[client_ip]['requests'] > self.limit
