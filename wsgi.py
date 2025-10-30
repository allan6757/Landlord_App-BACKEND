from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'demo_token',
        'user': {'id': 1, 'email': data.get('email'), 'role': 'tenant'}
    })

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    return jsonify({
        'success': True,
        'token': 'demo_token',
        'user': {'id': 1, 'email': data.get('email'), 'role': 'tenant'}
    })

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)