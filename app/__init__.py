from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()


login_manager = LoginManager()

# Per the LoginManager docs this function is required
@login_manager.user_loader
def load_user(user_id):
    return models.User.get(user_id)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes import main_routes, auth_routes, product_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(product_routes)
    
    return app

from app import models
