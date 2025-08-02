import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # 👈 force include root folder

from app import create_app, db
from app.models import User, Ticket

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Database tables created.")
