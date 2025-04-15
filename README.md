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
gemstone-jewelry-material-platform/
├── app/                          # Main application directory
│ ├── static/                     # Static files (CSS, JS, images)
│ ├── templates/                  # HTML templates
│ │ ├── base.html                 # Base template
│ │ ├── dashboard.html            # Dashboard page
│ │ ├── home.html                 # Home page
│ │ ├── merchant_profile.html     # Merchant profile page
│ │ └── search.html               # Search page
│ ├── uploads/                    # File uploads directory
│ ├── auth/                       # Authentication module
│ ├── payments/                   # Payments module
│ ├── products/                   # Products module
│ ├── init.py                     # Package initialization
│ ├── config.py                   # Configuration settings
│ ├── forms.py                    # Form definitions
│ ├── models.py                   # Database models
│ ├── routes.py                   # Application routes
│ ├── utils.py                    # Utility functions
│ └── run.py                      # Application entry point
├── requirements.txt              # Python dependencies
├── LICENSE                       # License file
└── README.md                     # Project documentation


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
