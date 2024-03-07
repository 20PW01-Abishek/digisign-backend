# controllers/base_controller.py
from flask import Blueprint

base_bp = Blueprint('base', __name__)

class BaseController:
    @staticmethod
    @base_bp.route('/')
    def index():
        return 'Hello, this is the root route!'
