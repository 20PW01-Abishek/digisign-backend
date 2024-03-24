from flask import Flask, jsonify
from controllers.base_controller import base_bp
from controllers.api.pdf_controller import pdf_bp
from db.connection import DatabaseConnection
from dotenv import load_dotenv
import os
from firebase_admin import credentials, initialize_app
from flask_cors import CORS

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Load Firebase service account credentials from environment variables
firebase_credentials = {
    "type": "service_account",
    "project_id": os.getenv('PROJECT_ID'),
    "private_key_id": os.getenv('PRIVATE_KEY_ID'),
    "private_key": os.getenv('PRIVATE_KEY').replace(r'\n', '\n'),
    "client_email": os.getenv('CLIENT_EMAIL'),
    "client_id": os.getenv('CLIENT_ID'),
    "auth_uri": os.getenv('AUTH_URI'),
    "token_uri": os.getenv('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL')
}

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate(firebase_credentials)
initialize_app(cred)

# enable CORS
CORS(app)

# register blueprint
app.register_blueprint(base_bp)
app.register_blueprint(pdf_bp)

if __name__ == '__main__':
    app.run(debug=True)