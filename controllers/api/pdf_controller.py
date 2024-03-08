# api/pdf_controller.py
from flask import Blueprint, request, jsonify, Response
from controllers.base_controller import BaseController
from db.connection import DatabaseConnection
from pymongo.errors import PyMongoError
from gridfs import GridFS
from bson import ObjectId
import io
import os

pdf_bp = Blueprint('pdf', __name__)

class PDFController(BaseController):
    @staticmethod
    @pdf_bp.route('/pdfs/create', methods=['POST'])
    def upload_pdf():
        try:
            user_id = '123'
            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            fs = GridFS(db)

            file = request.files['pdf']
            file_data = file.read()

            file_id = fs.put(file_data, filename=file.filename, user_id=user_id)
            
            return jsonify({'file_id': str(file_id)}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500


    @staticmethod
    @pdf_bp.route('/pdfs/user', methods=['GET'])
    def get_pdfs_by_user():
        try:
            user_id = request.args.get('user_id')
            if user_id is None:
                return jsonify({'error': 'User ID is required as a query parameter'}), 400
            
            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            fs = GridFS(db)

            pdf_files = fs.find({'user_id': user_id})
            pdf_list = [{'file_id': str(pdf._id), 'filename': pdf.filename} for pdf in pdf_files]

            return jsonify({'pdfs': pdf_list}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @pdf_bp.route('/pdfs', methods=['GET'])
    def get_pdf_by_id():
        try:
            file_id = request.args.get('file_id')
            if file_id is None:
                return jsonify({'error': 'File ID is required as a query parameter'}), 400
            
            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            fs = GridFS(db)

            pdf_file = fs.find_one({'_id': ObjectId(file_id)})
            if pdf_file is None:
                return jsonify({'error': 'PDF not found'}), 404
            
            pdf_data = fs.get(ObjectId(file_id)).read()
            
            # Send the PDF content as a response
            return Response(pdf_data, mimetype='application/pdf'), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500
