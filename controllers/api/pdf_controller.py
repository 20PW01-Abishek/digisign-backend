# api/pdf_controller.py
from flask import Blueprint, request, jsonify
from controllers.base_controller import BaseController
from db.connection import DatabaseConnection
from pymongo.errors import PyMongoError
from gridfs import GridFS
import io
import os

pdf_bp = Blueprint('pdf', __name__)

class PDFController(BaseController):
    @staticmethod
    @pdf_bp.route('/pdfs/create', methods=['POST'])
    def upload_pdf():
        try:
            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            fs = GridFS(db)

            file = request.files['pdf']
            file_data = file.read()

            file_id = fs.put(file_data, filename=file.filename)
            
            return jsonify({'file_id': str(file_id)}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

