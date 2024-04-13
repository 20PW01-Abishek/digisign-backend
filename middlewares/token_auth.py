# middlewares/token_auth.py
from flask import request, jsonify
from firebase_admin import auth

def verify_firebase_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None, str(e)

def check_token():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'message': 'Preflight request successful'})
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        return response

    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Missing token'}), 401

    verification_result = verify_firebase_token(token)

    if isinstance(verification_result, tuple):
        decoded_token, error_message = verification_result
        if not decoded_token:
            return jsonify({'message': error_message}), 401
    else:
        decoded_token = verification_result

    return None
