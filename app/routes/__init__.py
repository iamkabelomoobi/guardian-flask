from .auth import auth_bp

def register_routes(app):
    """
    Register all routes with the Flask app.
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')