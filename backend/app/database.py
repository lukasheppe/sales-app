import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration via environment variable
SQLALCHEMY_DATABASE_URL = os.getenv('DB_URL')
if SQLALCHEMY_DATABASE_URL is None:
    raise RuntimeError('Environment variable DB_URL is not set.')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Template to create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for sql alchemy models
Base = declarative_base()


def get_db():
    """
    Dependency injection provider for database sessions.
    :return: database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
