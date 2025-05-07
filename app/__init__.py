from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
import stripe

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    stripe.api_key = app.config.get('STRIPE_SECRET_KEY', '')

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.routes import main_routes, auth_routes, product_routes, payment_routes
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(product_routes)
    app.register_blueprint(payment_routes)

    with app.app_context():
        from app.models import User, Merchant, Product
        db.create_all()

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app