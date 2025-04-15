#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, session, flash, redirect, url_for, render_template_string, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_talisman import Talisman
import stripe
from login import login_required
from models import db, User, Merchant, Product

app = Flask(__name__)
app.secret_key = 'CHANGE_THIS_IN_PRODUCTION'
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
#Talisman(app)
# ----------------------------------------------------------------------------
# Database Configuration
# ----------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gemstone_platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Folder for uploaded images
app.config['UPLOAD_FOLDER'] = 'static_uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

# ----------------------------------------------------------------------------
# Database Models
# ----------------------------------------------------------------------------

def allowed_file(filename):
    """Check allowed file extensions for images."""
    ALLOWED = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED

# ----------------------------------------------------------------------------
# Single Template
# ----------------------------------------------------------------------------
# We'll use "page" + extra context to decide which content block to display.
# This includes pages: home, register, login, dashboard, merchant_profile,
# upload_product, products, product_detail, merchant_detail, search.

SINGLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Gemstone & Jewelry Platform</title>
  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
  <style>
    body {
      margin: 0;
      padding: 0;
    }
    .navbar-brand {
      font-weight: bold;
    }
    .container {
      margin-top: 1rem;
    }
    .card-img-top {
      max-height: 200px;
      object-fit: cover;
    }
    .product-img-detail {
      max-width: 300px;
      max-height: 300px;
      object-fit: cover;
      margin-bottom: 1rem;
    }
  </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="{{ url_for('home') }}">Gemstone Market</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarNav" aria-controls="navbarNav"
            aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon">☰</span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('list_products') }}">Marketplace</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('search') }}">Search</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('cart') }}">Cart 🛒</a>
        </li>
        {% if session.get('user_id') %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('dashboard') }}">Dashboard</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
          </li>
          
        {% else %}
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('login') }}">Login</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{ url_for('register') }}">Register</a>
          </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

<div class="container">
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <div class="alert alert-info mt-3">
        {% for message in messages %}
          <div>{{ message }}</div>
        {% endfor %}
      </div>
    {% endif %}
  {% endwith %}

  {# HOME PAGE #}
  {% if page == 'home' %}
    <div class="text-center">
      <h1>Welcome to the Gemstone & Jewelry Marketplace</h1>
      <p>Discover, buy, and sell precious gemstones and jewelry from around the world.</p>
      {% if not session.get('user_id') %}
        <a href="{{ url_for('register') }}" class="btn btn-primary btn-lg">Get Started</a>
      {% else %}
        <p>You are logged in as {{ session.get('username') }}. Go to your <a href="{{ url_for('dashboard') }}">Dashboard</a>.</p>
      {% endif %}
    </div>

  {# REGISTER PAGE #}
  {% elif page == 'register' %}
    <h2>Register</h2>
    <form method="POST" action="{{ url_for('register') }}" class="mb-3">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" name="email" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <button type="submit" class="btn btn-success">Register</button>
    </form>

  {# LOGIN PAGE #}
  {% elif page == 'login' %}
    <h2>Login</h2>
    <form method="POST" action="{{ url_for('login') }}" class="mb-3">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input type="text" name="username" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" name="password" class="form-control" required>
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>

  {# DASHBOARD PAGE #}
  {% elif page == 'dashboard' %}
    <h2>Dashboard</h2>
    {% if merchant %}
      <div class="mb-3">
        <h4>Your Merchant Profile</h4>
        <p><strong>Merchant Name:</strong> {{ merchant.merchant_name }}</p>
        <p><strong>Description:</strong> {{ merchant.description }}</p>
        <p><strong>Contact Info:</strong> {{ merchant.contact_info }}</p>
        <a href="{{ url_for('create_merchant_profile') }}" class="btn btn-secondary">Edit Profile</a>
      </div>
      <div class="mb-3">
        <a href="{{ url_for('upload_product') }}" class="btn btn-success">Upload New Product</a>
        <a href="{{ url_for('list_products') }}" class="btn btn-info">View All Products</a>
      </div>
    {% else %}
      <p>You don’t have a merchant profile yet.</p>
      <a href="{{ url_for('create_merchant_profile') }}" class="btn btn-primary">Create Profile</a>
    {% endif %}

  {# MERCHANT PROFILE PAGE #}
  {% elif page == 'merchant_profile' %}
    <h2>Merchant Profile</h2>
    <form method="POST" action="{{ url_for('create_merchant_profile') }}">
      <div class="mb-3">
        <label class="form-label">Merchant Name</label>
        <input type="text" name="merchant_name" class="form-control" required
               value="{{ merchant.merchant_name if merchant else '' }}">
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea name="description" rows="3" class="form-control">{{ merchant.description if merchant else '' }}</textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Contact Info</label>
        <input type="text" name="contact_info" class="form-control"
               value="{{ merchant.contact_info if merchant else '' }}">
      </div>
      <button type="submit" class="btn btn-success">Save Profile</button>
    </form>

  {# UPLOAD PRODUCT PAGE #}
  {% elif page == 'upload_product' %}
    <h2>Upload New Product</h2>
    <form method="POST" action="{{ url_for('upload_product') }}" enctype="multipart/form-data" class="mb-3">
      <div class="mb-3">
        <label class="form-label">Product Name</label>
        <input type="text" name="name" class="form-control" required>
      </div>
      <div class="mb-3">
        <label class="form-label">Description</label>
        <textarea name="description" rows="3" class="form-control"></textarea>
      </div>
      <div class="mb-3">
        <label class="form-label">Price (USD)</label>
        <input type="number" name="price" step="0.01" class="form-control" required>
      </div>
      <!-- Extended fields -->
      <div class="mb-3">
        <label class="form-label">Materials (e.g. List materials like this: Gold, Silver, Diamond)</label>
        <input type="text" name="material" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Weight (e.g. "2 grams")</label>
        <input type="text" name="weight" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Carat (e.g. "24k" or "10ct")</label>
        <input type="text" name="carat" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Color (e.g. "Red", "White")</label>
        <input type="text" name="color" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Clarity (e.g. "VVS1")</label>
        <input type="text" name="clarity" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Country of Origin</label>
        <input type="text" name="country_of_origin" class="form-control">
      </div>
      <div class="mb-3">
        <label class="form-label">Product Image</label>
        <input type="file" name="image" accept=".png,.jpg,.jpeg,.gif,.webp" class="form-control">
      </div>
      <button type="submit" class="btn btn-primary">Upload Product</button>
    </form>

  {# LIST PRODUCTS PAGE (MARKETPLACE) #}
  {% elif page == 'products' %}
    <h2>Marketplace</h2>
    {% if products %}
      <div class="row">
        {% for product in products %}
          <div class="col-md-4 mb-4">
            <div class="card">
              {% if product.image_filename %}
                <a href="{{ url_for('product_detail', product_id=product.id) }}">
                  <img src="/{{ upload_folder }}/{{ product.image_filename }}" class="card-img-top" alt="{{ product.name }}">
                </a>
              {% else %}
                <a href="{{ url_for('product_detail', product_id=product.id) }}">
                  <img src="https://via.placeholder.com/300x200?text=No+Image" class="card-img-top" alt="Placeholder">
                </a>
              {% endif %}
              <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-text">{{ product.description[:80] }}{% if product.description|length > 80 %}...{% endif %}</p>
                <p><strong>Price:</strong> ${{ "%.2f"|format(product.price) }}</p>
                <p>
                  <strong>Merchant:</strong>
                  <a href="{{ url_for('merchant_detail', merchant_id=product.merchant.id) }}">
                    {{ product.merchant.merchant_name }}
                  </a>
                </p>
                <a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-outline-primary btn-sm">
                  View Details
                </a>
              </div>
            </div>
          </div>
        {% endfor %}
      </div>
    {% else %}
      <p>No products found.</p>
    {% endif %}

  {# INDIVIDUAL PRODUCT DETAIL PAGE #}
  {% elif page == 'product_detail' %}
    {% if product %}
      <h2>{{ product.name }}</h2>
      {% if product.image_filename %}
        <img src="/{{ upload_folder }}/{{ product.image_filename }}" class="product-img-detail" alt="{{ product.name }}">
      {% else %}
        <img src="https://via.placeholder.com/300?text=No+Image" class="product-img-detail" alt="{{ product.name }}">
      {% endif %}
      <p><strong>Description:</strong> {{ product.description }}</p>
      <p><strong>Price:</strong> ${{ "%.2f"|format(product.price) }}</p>
      <p><strong>Material:</strong> {{ product.material }}</p>
      <p><strong>Weight:</strong> {{ product.weight }}</p>
      <p><strong>Carat:</strong> {{ product.carat }}</p>
      <p><strong>Color:</strong> {{ product.color }}</p>
      <p><strong>Clarity:</strong> {{ product.clarity }}</p>
      <p><strong>Country of Origin:</strong> {{ product.country_of_origin }}</p>
      <hr>
      <p><strong>Sold by:</strong>
        <a href="{{ url_for('merchant_detail', merchant_id=product.merchant.id) }}">
          {{ product.merchant.merchant_name }}
        </a>
      </p>
      <a href="{{ url_for('list_products') }}" class="btn btn-secondary">Back to Marketplace</a>
      <a href="{{ url_for('add_to_cart', product_id=product.id) }}" class="btn btn-outline-success btn-sm">Add to Cart 🛒</a>
    {% else %}
      <p>Product not found.</p>
    {% endif %}

  {# MERCHANT DETAIL PAGE #}
  {% elif page == 'merchant_detail' %}
    {% if merchant %}
      <h2>Merchant: {{ merchant.merchant_name }}</h2>
      <p><strong>Description:</strong> {{ merchant.description }}</p>
      <p><strong>Contact:</strong> {{ merchant.contact_info }}</p>
      <hr>
      <h4>Products by {{ merchant.merchant_name }}</h4>
      {% if merchant.products %}
        <div class="row">
          {% for product in merchant.products %}
            <div class="col-md-4 mb-4">
              <div class="card">
                {% if product.image_filename %}
                  <a href="{{ url_for('product_detail', product_id=product.id) }}">
                    <img src="/{{ upload_folder }}/{{ product.image_filename }}" class="card-img-top" alt="{{ product.name }}">
                  </a>
                {% else %}
                  <a href="{{ url_for('product_detail', product_id=product.id) }}">
                    <img src="https://via.placeholder.com/300x200?text=No+Image" class="card-img-top" alt="Placeholder">
                  </a>
                {% endif %}
                <div class="card-body">
                  <h5 class="card-title">{{ product.name }}</h5>
                  <p class="card-text">{{ product.description[:80] }}{% if product.description|length > 80 %}...{% endif %}</p>
                  <p><strong>Price:</strong> ${{ "%.2f"|format(product.price) }}</p>
                  <a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-outline-primary btn-sm">
                    View Details
                  </a>
                </div>
              </div>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <p>This merchant has no products listed yet.</p>
      {% endif %}
    {% else %}
      <p>Merchant not found.</p>
    {% endif %}

  {# Cart PAGE #}
  {% elif page == 'cart' %}
    <h2>Your Cart</h2>
    {% if products %}
      <ul class="list-group mb-3">
        {% for product in products %}
          <li class="list-group-item d-flex justify-content-between align-items-center">
            {{ product.name }} - ${{ "%.2f"|format(product.price) }}
            <a href="{{ url_for('remove_from_cart', product_id=product.id) }}" class="btn btn-sm btn-danger">Remove</a>
          </li>
        {% endfor %}
      </ul>
      <p><strong>Total: ${{ "%.2f"|format(total) }}</strong></p>
      <form action="{{ url_for('checkout') }}" method="post">
        <button type="submit" class="btn btn-primary">Proceed to Checkout</button>
      </form>
    {% else %}
      <p>Your cart is empty.</p>
    {% endif %}



  {# SEARCH PAGE #}
  {% elif page == 'search' %}
    <h2>Search</h2>
    <form method="POST" action="{{ url_for('search') }}" class="mb-3">
      <div class="mb-3">
        <input type="text" name="query" class="form-control" placeholder="Search products by name, material..." value="{{ query|default('') }}">
      </div>
      <button type="submit" class="btn btn-primary">Search</button>
    </form>
    {% if query %}
      <h5>Results for "{{ query }}":</h5>
      {% if products %}
        <div class="row">
          {% for product in products %}
            <div class="col-md-4 mb-4">
              <div class="card">
                {% if product.image_filename %}
                  <a href="{{ url_for('product_detail', product_id=product.id) }}">
                    <img src="/{{ upload_folder }}/{{ product.image_filename }}" class="card-img-top" alt="{{ product.name }}">
                  </a>
                {% else %}
                  <a href="{{ url_for('product_detail', product_id=product.id) }}">
                    <img src="https://via.placeholder.com/300x200?text=No+Image" class="card-img-top" alt="Placeholder">
                  </a>
                {% endif %}
                <div class="card-body">
                  <h5 class="card-title">{{ product.name }}</h5>
                  <p class="card-text">{{ product.description[:80] }}{% if product.description|length > 80 %}...{% endif %}</p>
                  <p><strong>Price:</strong> ${{ "%.2f"|format(product.price) }}</p>
                  <p><strong>Merchant:</strong> {{ product.merchant.merchant_name }}</p>
                  <a href="{{ url_for('product_detail', product_id=product.id) }}" class="btn btn-outline-primary btn-sm">
                    View Details
                  </a>
                </div>
              </div>
            </div>
          {% endfor %}
        </div>
      {% else %}
        <p>No matching products found.</p>
      {% endif %}
    {% endif %}
  {% endif %}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------

@app.route('/')
@login_required
def home():
    """Landing page."""
    return render_template_string(SINGLE_TEMPLATE, page='home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        # Check if username/email already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        if existing_user:
            flash("Username or email already in use.")
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))

    return render_template_string(SINGLE_TEMPLATE, page='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash("Login successful.")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))

    return render_template_string(SINGLE_TEMPLATE, page='login')

@app.route('/logout')
def logout():
    """Log out user."""
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """User dashboard."""
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    user_id = session['user_id']
    merchant = Merchant.query.filter_by(user_id=user_id).first()
    return render_template_string(SINGLE_TEMPLATE, page='dashboard', merchant=merchant)

@app.route('/create_merchant_profile', methods=['GET', 'POST'])
def create_merchant_profile():
    """Create or update the merchant profile."""
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    user_id = session['user_id']
    merchant = Merchant.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        m_name = request.form['merchant_name'].strip()
        desc = request.form['description'].strip()
        contact = request.form['contact_info'].strip()

        if merchant:
            # update existing
            merchant.merchant_name = m_name
            merchant.description = desc
            merchant.contact_info = contact
        else:
            # create new
            merchant = Merchant(
                user_id=user_id,
                merchant_name=m_name,
                description=desc,
                contact_info=contact
            )
            db.session.add(merchant)
        db.session.commit()
        flash("Merchant profile saved!")
        return redirect(url_for('dashboard'))

    return render_template_string(SINGLE_TEMPLATE, page='merchant_profile', merchant=merchant)

@app.route('/upload_product', methods=['GET', 'POST'])
def upload_product():
    """Upload a new gemstone/jewelry product with extended fields."""
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))

    merchant = Merchant.query.filter_by(user_id=session['user_id']).first()
    if not merchant:
        flash("You need a merchant profile first.")
        return redirect(url_for('create_merchant_profile'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        desc = request.form['description'].strip()
        price = float(request.form['price'].strip())

        # Extra fields
        material = request.form['material'].strip() or None
        weight = request.form['weight'].strip() or None
        carat = request.form['carat'].strip() or None
        color = request.form['color'].strip() or None
        clarity = request.form['clarity'].strip() or None
        origin = request.form['country_of_origin'].strip() or None

        file = request.files.get('image')
        filename = None
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
            else:
                flash("Invalid file type. Only png/jpg/jpeg/gif/webp are allowed.")
                return redirect(url_for('upload_product'))

        new_product = Product(
            merchant_id=merchant.id,
            name=name,
            description=desc,
            price=price,
            image_filename=filename,
            material=material,
            weight=weight,
            carat=carat,
            color=color,
            clarity=clarity,
            country_of_origin=origin
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product uploaded successfully.")
        return redirect(url_for('list_products'))

    return render_template_string(SINGLE_TEMPLATE, page='upload_product')

@app.route('/products')
@login_required
def list_products():
    """View the main marketplace page, which lists all products."""
    products = Product.query.all()
    return render_template_string(
        SINGLE_TEMPLATE,
        page='products',
        products=products,
        upload_folder=app.config['UPLOAD_FOLDER']
    )

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """View a single product detail."""
    product = Product.query.get(product_id)
    return render_template_string(
        SINGLE_TEMPLATE,
        page='product_detail',
        product=product,
        upload_folder=app.config['UPLOAD_FOLDER']
    )

@app.route('/merchant/<int:merchant_id>')
def merchant_detail(merchant_id):
    """View a merchant's profile and their products."""
    merchant = Merchant.query.get(merchant_id)
    return render_template_string(
        SINGLE_TEMPLATE,
        page='merchant_detail',
        merchant=merchant,
        upload_folder=app.config['UPLOAD_FOLDER']
    )

@app.route('/search', methods=['GET', 'POST'])
def search():
    """Search for products by name or material."""
    query = ""
    results = []
    if request.method == 'POST':
        query = request.form['query'].strip()
        if query:
            # basic search in name OR material
            results = Product.query.filter(
                (Product.name.ilike(f"%{query}%")) | (Product.material.ilike(f"%{query}%"))
            ).all()

    return render_template_string(
        SINGLE_TEMPLATE,
        page='search',
        products=results,
        query=query,
        upload_folder=app.config['UPLOAD_FOLDER']
    )

@app.route('/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash("Cart is empty.")
        return redirect(url_for('cart'))

    products = Product.query.filter(Product.id.in_(cart)).all()

    line_items = []
    for product in products:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product.name,
                },
                "unit_amount": int(product.price * 100),
            },
            "quantity": 1,
        })

    session_obj = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=url_for('payment_success', _external=True),
        cancel_url=url_for('cart', _external=True)
    )

    return redirect(session_obj.url, code=303)

@app.route('/payment-success')
def payment_success():
    return "<h1>Payment Successful!</h1>"

@app.route('/payment-cancel')
def payment_cancel():
    return "<h1>Payment Canceled.</h1>"

@app.route('/add-to-cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    session['cart'] = cart
    flash("Item added to cart.")
    return redirect(url_for('list_products'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    total = sum([p.price for p in products])
    return render_template_string(SINGLE_TEMPLATE, page='cart', products=products, total=total)

@app.route('/remove-from-cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    session['cart'] = cart
    flash("Item removed from cart.")
    return redirect(url_for('cart'))


# ----------------------------------------------------------------------------
# Initialize & Run
# ----------------------------------------------------------------------------

def init_db():
    """Create tables if they don't exist."""
    db.create_all()
    print("Database initialized!")
if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)
