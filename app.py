from flask import Flask, jsonify
from controllers.base_controller import base_bp
from db.connection import DatabaseConnection
from controllers.api.pdf_controller import pdf_bp
from dotenv import load_dotenv

app = Flask(__name__)

app.register_blueprint(base_bp)
app.register_blueprint(pdf_bp)

if __name__ == '__main__':
    app.run(debug=True)