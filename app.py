from flask import Flask
from controllers.base_controller import base_bp

app = Flask(__name__)

app.register_blueprint(base_bp)

if __name__ == '__main__':
    app.run(debug=True)