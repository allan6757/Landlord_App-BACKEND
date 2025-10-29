from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['*'])

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'message': 'Registration endpoint working',
        'data': data
    }), 201

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'message': 'Login endpoint working',
        'data': data
    }), 200

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Minimal app working'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)