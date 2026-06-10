import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Get the online database URL from environment variables.
# If it doesn't exist, it safely falls back to your local SQLite database.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "https://tctbchymaknvenmbavay.supabase.coss", 
    "sqlite:///./agri_app.db"
)

# 2. Fix for PostgreSQL connections (Production environments like Heroku/Render)
# Production platforms sometimes use 'postgres://', but SQLAlchemy requires 'postgresql://'
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Create the engine configuration
# 'check_same_thread' is ONLY needed for SQLite. We disable it if using an online DB.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. Initialize session and base engine tools
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 5. Dependency helper to inject database sessions into our API endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()