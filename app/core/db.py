import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# SUMMARY:
# Load environment variables from a .env file and set up the database connection string for PostgreSQL using SQLAlchemy.

load_dotenv()

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")

CONNECTION_STRING = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(CONNECTION_STRING)

def init_db_extension():
    """Initialize the pgvector extension in the PostgreSQL database."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        conn.commit()
    