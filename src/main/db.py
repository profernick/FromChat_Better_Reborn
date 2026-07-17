import os
from typing import Generator, Optional

import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

from .constants import DATABASE_URL

logger = logging.getLogger(__name__)

"""
PostgreSQL database interface for the main service.

Exposes `engine`, `SessionLocal`, `get_db` dependency, and `POOL_CONFIG`.
"""

# Pool and engine configuration (tunable via env)
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "20"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "40"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))

POOL_CONFIG = {
    "pool_size": POOL_SIZE,
    "max_overflow": MAX_OVERFLOW,
    "pool_recycle": POOL_RECYCLE,
    "pool_timeout": POOL_TIMEOUT,
    "pool_pre_ping": True,
}


def get_engine(database_url: Optional[str] = None) -> Engine:
    """
    Create and return a SQLAlchemy Engine for PostgreSQL.
    Includes retry logic for database connection failures during startup.
    """
    url = database_url or DATABASE_URL

    max_retries = 15
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting database connection (attempt {attempt + 1}/{max_retries})...")
            test_engine = create_engine(url, pool_size=1, max_overflow=0, pool_timeout=5, future=True)
            with test_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            test_engine.dispose()
            logger.info("Database connection successful")
            break
        except OperationalError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection failed (attempt {attempt + 1}): {e}")
                time.sleep(retry_delay)
            else:
                logger.error(f"Database connection failed after {max_retries} attempts: {e}")
                raise
        except Exception as e:
            logger.error(f"Unexpected error during database connection: {e}")
            raise

    engine_kwargs = {
        "pool_size": POOL_SIZE,
        "max_overflow": MAX_OVERFLOW,
        "pool_recycle": POOL_RECYCLE,
        "pool_timeout": POOL_TIMEOUT,
        "future": True,
    }
    return create_engine(url, **engine_kwargs)


# Create global engine and session factory for convenient imports
engine = get_engine()
# Keep loaded attributes available after commit/close to avoid DetachedInstanceError
SessionLocal = sessionmaker(class_=Session, autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def init_db(create_tables: bool = False, base_metadata=None) -> None:
    """
    Initialize the database. If `create_tables` is True and `base_metadata` is provided,
    create all tables using the provided SQLAlchemy metadata.
    """
    if create_tables:
        if base_metadata is None:
            raise ValueError("base_metadata is required to create tables")
        base_metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and ensures proper close().
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception:
            pass
