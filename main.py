from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return response

@app.route('/')
def home():
    return jsonify({'message': 'Backend is running'})

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'demo_token_123',
        'user': {
            'id': 1,
            'email': data.get('email', 'user@example.com'),
            'role': data.get('role', 'tenant'),
            'first_name': data.get('first_name', 'User'),
            'last_name': data.get('last_name', 'Name')
        }
    }), 201

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'demo_token_123',
        'user': {
            'id': 1,
            'email': data.get('email', 'user@example.com'),
            'role': 'tenant',
            'first_name': 'Demo',
            'last_name': 'User'
        }
    }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)