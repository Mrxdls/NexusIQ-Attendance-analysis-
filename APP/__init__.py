from flask import Flask
from APP.routes import app_routes  # Import the routes Blueprint


import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    print("Template folder path:", os.path.abspath(app.template_folder))  # Debugging
    app.secret_key = 'your_secret_key'
    app.register_blueprint(app_routes)
    return app