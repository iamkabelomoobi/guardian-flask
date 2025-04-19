from flask import Flask
from .extensions import db, migrate
from app.routes import register_routes

def create_app(config_class='app.config.DevConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    register_routes(app)
    
    return app