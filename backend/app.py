from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to GradientLab API',
        'status': 'online',
        'version': '0.1.0'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy'
    })

if __name__ == '__main__':
    app.run(debug=True)
