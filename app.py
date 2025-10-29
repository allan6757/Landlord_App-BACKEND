from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'test_token_123',
        'user': {
            'id': 1,
            'email': data.get('email', 'test@example.com'),
            'role': data.get('role', 'tenant')
        }
    }), 201

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'test_token_123',
        'user': {
            'id': 1,
            'email': data.get('email', 'test@example.com'),
            'role': 'tenant'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Working'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)