"""GasPot HMI Dashboard - Flask Application Factory"""

import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database configuration from environment
DB_HOST = os.environ.get("DB_HOST", "gaspot-historian")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_USER = os.environ.get("DB_USER", "lab")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_NAME = os.environ.get("DB_NAME", "historian")

# GasPot configuration from environment
GASPOT_HOST = os.environ.get("GASPOT_HOST", "gaspot-simulator")
GASPOT_PORT = int(os.environ.get("GASPOT_PORT", "10001"))

# Database engine (created on first request)
_engine = None
_Session = None


def get_db_engine():
    """Get or create database engine."""
    global _engine
    if _engine is None:
        db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        _engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)
    return _engine


def get_db_session():
    """Get a new database session."""
    global _Session
    if _Session is None:
        _Session = sessionmaker(bind=get_db_engine())
    return _Session()


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Store config in app
    app.config["GASPOT_HOST"] = GASPOT_HOST
    app.config["GASPOT_PORT"] = GASPOT_PORT

    # Register routes
    from app import routes
    app.register_blueprint(routes.bp)

    # Start background poller (only in main process, not reloader)
    import os
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true' or not app.debug:
        from app.poller import start_poller
        start_poller()

    return app
