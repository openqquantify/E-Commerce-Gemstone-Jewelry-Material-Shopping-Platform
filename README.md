# Gemstone-Jewelry-Material-Platform

![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-blueviolet)
![Stripe](https://img.shields.io/badge/Stripe-5.5.0-blue)
![Web3](https://img.shields.io/badge/Web3-6.4.0-orange)

A modern e-commerce platform for buying and selling precious gemstones and jewelry with merchant support, secure payments, and Web3 integration.

## ✨ Features

### User System
- 🔐 Secure authentication (register/login/logout)
- 👤 User profiles with roles (buyer/merchant)
- 🔑 Password hashing with PBKDF2-SHA256

### Merchant Portal
- 🏪 Create merchant profiles
- 📦 Product management dashboard
- 🖼️ Image upload with auto-thumbnails

### Marketplace
- 🔍 Advanced search by material/attributes
- 🛒 Shopping cart functionality
- 💳 Stripe & crypto payment options
- 📱 Fully responsive design

### Product Listings
- 💎 Detailed gemstone specifications:
  - Material composition
  - Weight/carat measurements
  - Color/clarity grades
  - Country of origin

## 🛠️ Tech Stack

### Backend
- Python 3.10+
- Flask framework
- SQLAlchemy ORM
- Stripe API integration
- Web3.py for crypto payments

### Frontend
- Bootstrap 5.3
- Font Awesome 6
- Custom CSS animations
- Vanilla JavaScript

### Database
- SQLite (development)
- MySQL (production)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip package manager
- MySQL (for production)

## 📁 Project Structure

```bash
gemstone-marketplace/
├── app/                      # Core application package
│   ├── __init__.py           # Flask app factory and initialization
│   ├── routes.py             # All application routes (organized as Blueprints)
│   ├── models.py             # Database models (User, Merchant, Product)
│   ├── forms.py              # WTForms classes for all forms
│   ├── utils/                # Utility modules
│   │   ├── auth.py           # Authentication helpers (password hashing, tokens)
│   │   ├── payments.py       # Payment processors (Stripe, Web3)
│   │   ├── file_uploads.py   # Secure file upload handling
│   │   └── validators.py     # Custom form validators
│   ├── static/
│   │   ├── css/              # Custom styles (Bootstrap overrides)
│   │   ├── js/               # Client-side functionality
│   │   └── images/           # Logos, default product images
│   ├── templates/            # Jinja2 templates
│   │   ├── layouts/          # Base templates
│   │   │   ├── base.html     # Main layout
│   │   │   └── auth.html     # Auth-specific layout
│   │   ├── components/       # Reusable UI components
│   │   ├── auth/             # Authentication flows
│   │   ├── products/         # Marketplace views
│   │   └── payments/         # Checkout process
│   └── uploads/              # User-generated content (gitignored)
├── tests/                    # Pytest unit and integration tests
├── migrations/               # Database migration scripts (Alembic)
├── config.py                 # Flask configuration settings
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── run.py                    # Application entry point
└── .env.example              # Environment variables template



### Key Directories Explained:

1. **`app/`** - Core application package
   - `routes.py`: Organized using Flask Blueprints (auth, main, products)
   - `models.py`: Contains all SQLAlchemy models (User, Merchant, Product)
   - `utils/`: Modular utilities for payments, auth, and file handling

2. **`static/`** - Frontend assets
   - Designed with mobile-first responsive approach
   - Vanilla JavaScript (no jQuery dependency)

3. **`templates/`** - Jinja2 templates
   - Uses template inheritance (`base.html`)
   - Modular partials for reusable components
   - Organized by feature (auth, products, payments)

4. **Configuration**
   - `config.py`: Centralized configuration
   - `.env.example`: Template for environment variables
   - `requirements.txt`: Pinned dependencies

### Best Practices:
- **Separation of Concerns**: Clear division between routes, models, and templates
- **Modular Design**: Features split into logical components
- **Security**: Uploads stored outside static folder
- **Scalability**: Ready for MySQL migration in production


### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/gemstone-marketplace.git
cd gemstone-marketplace

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials
