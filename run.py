from app import create_app
from app import db

app = create_app()

def init_db():
    """Create tables if they don't exist."""
    db.create_all()
    print("Database initialized!")

if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True)