# api/pdf_controller.py
from flask import Blueprint, request, jsonify, Response
from controllers.base_controller import BaseController, base_bp
from db.connection import DatabaseConnection
from pymongo.errors import PyMongoError
from gridfs import GridFS
from bson import ObjectId
import io
import os

pdf_bp = Blueprint("pdf", __name__)

class PDFController(BaseController):
    @staticmethod
    @base_bp.route('/pdfs/create', methods=['POST'])
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
    @base_bp.route('/pdfs/user', methods=['GET'])
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
    @base_bp.route('/pdfs', methods=['GET'])
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
            
            return Response(pdf_data, mimetype='application/pdf'), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @base_bp.route('/pdfs/share', methods=['POST'])
    def share_pdf():
        try:
            emails = request.json.get('emails')
            file_ids = request.json.get('file_ids')

            if not emails or not file_ids:
                return jsonify({'error': 'Emails and file IDs are required'}), 400

            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            fs = GridFS(db)

            shared_pdf_collection = db.fs.files

            for file_id in file_ids:
                pdf_metadata = shared_pdf_collection.find_one({'_id': ObjectId(file_id)})
                if pdf_metadata:
                    shared_to = pdf_metadata.get('shared_to', {})

                    for email in emails:
                        if email not in shared_to or shared_to[email] is True:
                            shared_to[email] = False

                    shared_pdf_collection.update_one(
                        {'_id': ObjectId(file_id)},
                        {'$set': {'shared_to': shared_to}}
                    )

            return jsonify({'message': 'PDFs shared successfully'}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @base_bp.route('/pdfs/remove_share', methods=['POST'])
    def remove_shared_access():
        try:
            emails = request.json.get('emails')
            file_ids = request.json.get('file_ids')

            if not emails or not file_ids:
                return jsonify({'error': 'Emails and file IDs are required'}), 400

            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()
            
            db = client.digisign_activity
            shared_pdf_collection = db.fs.files

            for file_id in file_ids:
                pdf_metadata = shared_pdf_collection.find_one({'_id': ObjectId(file_id)})
                if pdf_metadata:
                    
                    for email in emails:
                        if email in pdf_metadata.get('shared_to', {}):
                            del pdf_metadata['shared_to'][email]
                   
                    shared_pdf_collection.update_one(
                        {'_id': ObjectId(file_id)},
                        {'$set': {'shared_to': pdf_metadata.get('shared_to', {})}}
                    )

            return jsonify({'message': 'Shared access removed successfully'}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500

    @staticmethod
    @base_bp.route('/pdfs/sent_for_signing', methods=['GET'])
    def get_sent_for_signing_pdfs():
        try:
            user_id = request.args.get('user_id')

            if not user_id:
                return jsonify({'error': 'User ID is required as a query parameter'}), 400

            db_connection = DatabaseConnection(os.getenv("MONGODB_URI"))
            client = db_connection.get_connection()

            db = client.digisign_activity
            shared_pdf_collection = db.fs.files

            sent_for_signing_pdfs = shared_pdf_collection.find({
                'user_id': user_id,
                'shared_to': {'$exists': True, '$ne': {}}
            })

            pdf_list = [{
                'file_id': str(pdf['_id']),
                'filename': pdf['filename'],
                'shared_to': pdf.get('shared_to', {})
            } for pdf in sent_for_signing_pdfs]

            return jsonify({'pdfs': pdf_list}), 200
        except PyMongoError as e:
            return jsonify({'error': str(e)}), 500