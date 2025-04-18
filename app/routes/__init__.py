from flask import Blueprint

# Create a Blueprint for the routes
routes = Blueprint('routes', __name__)

@routes.route('/')
def hello_world():
    return "Hello, World!"