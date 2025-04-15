from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.models import db, User, Merchant, Product
from app.forms import RegistrationForm, LoginForm, ProductForm
from app.utils import save_image, allowed_file
import os
import stripe

# Initialize Blueprints
main_routes = Blueprint('main', __name__)
auth_routes = Blueprint('auth', __name__)
product_routes = Blueprint('products', __name__)
payment_routes = Blueprint('payments', __name__)

# Stripe configuration
stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

# Main Routes
@main_routes.route('/')
def home():
    return render_template('home.html')

@main_routes.route('/dashboard')
@login_required
def dashboard():
    merchant = Merchant.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', merchant=merchant)

@main_routes.route('/create_merchant_profile', methods=['GET', 'POST'])
@login_required
def create_merchant_profile():
    merchant = Merchant.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        m_name = request.form['merchant_name'].strip()
        desc = request.form['description'].strip()
        contact = request.form['contact_info'].strip()

        if merchant:
            merchant.merchant_name = m_name
            merchant.description = desc
            merchant.contact_info = contact
        else:
            merchant = Merchant(
                user_id=current_user.id,
                merchant_name=m_name,
                description=desc,
                contact_info=contact
            )
            db.session.add(merchant)
        
        db.session.commit()
        flash('Merchant profile saved!', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('merchant_profile.html', merchant=merchant)

# Auth Routes
@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already in use', 'danger')
            return redirect(url_for('auth.register'))
            
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Product Routes
@product_routes.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@product_routes.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail.html', product=product)

@product_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_product():
    form = ProductForm()
    merchant = Merchant.query.filter_by(user_id=current_user.id).first()
    
    if not merchant:
        flash('You need a merchant profile first.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            if allowed_file(form.image.data.filename):
                filename = save_image(form.image.data)
            else:
                flash('Invalid file type. Allowed: png, jpg, jpeg, webp', 'danger')
                return redirect(url_for('products.upload_product'))
        
        product = Product(
            merchant_id=merchant.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            image_filename=filename,
            material=form.material.data,
            weight=form.weight.data,
            carat=form.carat.data,
            color=form.color.data,
            clarity=form.clarity.data,
            country_of_origin=form.country_of_origin.data
        )
        
        db.session.add(product)
        db.session.commit()
        flash('Product uploaded successfully!', 'success')
        return redirect(url_for('products.list_products'))
    
    return render_template('products/upload.html', form=form)

# Payment Routes
@payment_routes.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    total = sum(p.price for p in products)
    return render_template('payments/cart.html', products=products, total=total)

@payment_routes.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart = session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    session['cart'] = cart
    flash('Item added to cart', 'success')
    return redirect(url_for('products.list_products'))

@payment_routes.route('/remove-from-cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    session['cart'] = cart
    flash('Item removed from cart', 'info')
    return redirect(url_for('payments.cart'))

@payment_routes.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('payments.cart'))
    
    products = Product.query.filter(Product.id.in_(cart)).all()
    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': product.name,
            },
            'unit_amount': int(product.price * 100),
        },
        'quantity': 1,
    } for product in products]
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('payments.payment_success', _external=True),
            cancel_url=url_for('payments.cart', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        flash(str(e), 'danger')
        return redirect(url_for('payments.cart'))

@payment_routes.route('/payment-success')
def payment_success():
    session['cart'] = []  # Clear cart after successful payment
    return render_template('payments/success.html')

@payment_routes.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query', '')
    results = []
    
    if query:
        results = Product.query.filter(
            (Product.name.ilike(f'%{query}%')) |
            (Product.material.ilike(f'%{query}%')) |
            (Product.description.ilike(f'%{query}%'))
        ).all()
    
    return render_template('search.html', results=results, query=query)
