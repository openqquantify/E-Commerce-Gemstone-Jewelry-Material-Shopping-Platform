from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User accounts for login."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    merchant = db.relationship('Merchant', backref='user', uselist=False)

class Merchant(db.Model):
    """One merchant profile per user."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    merchant_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    contact_info = db.Column(db.String(200))
    products = db.relationship('Product', backref='merchant', lazy=True)

class Product(db.Model):
    """A gemstone/jewelry product with extended fields."""
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300))
    
    # Extra details
    material = db.Column(db.String(120))         # e.g. gold, silver, diamond, ruby, etc.
    weight = db.Column(db.String(120))           # e.g. "2 grams", "10 carats"
    carat = db.Column(db.String(120))            # e.g. "24k" or "10ct"
    color = db.Column(db.String(120))            # e.g. "Red", "Blue", "White"
    clarity = db.Column(db.String(120))          # e.g. "VVS1", "IF", "Excellent"
    country_of_origin = db.Column(db.String(120)) # e.g. "Colombia", "India", "Brazil"
