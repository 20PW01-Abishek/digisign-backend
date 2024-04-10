# controllers/base_controller.py
from flask import Blueprint
from middlewares.token_auth import check_token
base_bp = Blueprint('base', __name__)

class BaseController:
    @staticmethod
    @base_bp.before_request
    def validate_token():
        response = check_token()
        if response:
            return response

    @staticmethod
    @base_bp.route('/')
    def index():
        return 'Hello, this is the root route!'
