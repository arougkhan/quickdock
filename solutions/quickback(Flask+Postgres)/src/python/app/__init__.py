# app/__init__.py
import os
from flask import Flask

def create_app(testing=False):
    app = Flask(__name__)
    CONFIG_TYPE = os.getenv('FLASK_CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(CONFIG_TYPE)

    # Register blueprints
    register_blueprints(app)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app

### Helper Functions ###
def register_blueprints(app):
    #from app.auth import auth_blueprint
    #from app.main import main_blueprint

    #app.register_blueprint(auth_blueprint, url_prefix='/users')
    #app.register_blueprint(main_blueprint)
    pass

def initialize_extensions(app):
    pass

def register_error_handlers(app):
    pass

def configure_logging(app):
    pass