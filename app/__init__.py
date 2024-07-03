from flask import Flask
from .database import init_db
import os

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    init_db(app)

    return app
