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

### Structure
gemstone-marketplace/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # All application routes
│   ├── models.py           # Database models
│   ├── forms.py            # WTForms classes
│   ├── utils/              # Helper modules
│   │   ├── auth.py         # Auth utilities
│   │   ├── payments.py     # Payment processors
│   │   └── web3.py         # Web3 integration
│   ├── static/
│   │   ├── css/main.css    # Custom styles
│   │   ├── js/main.js      # Client-side scripts
│   │   └── images/         # Static assets
│   ├── templates/          # Jinja2 templates
│   └── uploads/            # User uploads
├── config.py               # Configuration
├── requirements.txt        # Dependencies
└── run.py                  # Entry point

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
