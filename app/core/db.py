from sqlalchemy import create_engine, text
from core.config import settings

# SUMMARY:
# Database engine and the one-time setup of the pgvector extension.

engine = create_engine(settings.connection_string)


def init_db_extension():
    """Initialize the pgvector extension in the PostgreSQL database."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
