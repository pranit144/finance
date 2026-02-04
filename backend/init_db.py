"""
Create database tables for SQLite.
Run this once to initialize the database.
"""
from app.core.database import engine, Base
from app.models.user import User

print("Creating database tables...")

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")
print("You can now run the application.")
