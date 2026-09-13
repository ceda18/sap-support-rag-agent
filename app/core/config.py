from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# SUMMARY:
# Single source of truth for configuration. Everything from .env is loaded here once,
# and the rest of the project imports `settings` instead of reading the environment.


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ENVIRONMENT: str = "development"

    # Anthropic
    ANTHROPIC_API_KEY: str
    ANTHROPIC_MODEL: str = "claude-sonnet-5"
    MAX_TOKENS: int = 1024
    RULES_PATH: str = "/app/rag/agent_rules.txt"

    # Embeddings and retrieval
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    COLLECTION_NAME: str = "sap_rag_collection"
    TOP_K: int = 5
    BM25_WEIGHT: float = 0.4
    VECTOR_WEIGHT: float = 0.6
    MIN_SCORE: float = 0.3

    # Data paths (inside the container)
    PDF_PATH: str = "/data/Application_Help_for_SAP_PaPM.pdf"
    CHUNKS_PATH: str = "/app/data/chunks.json"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # PostgreSQL / pgvector
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str #= "db"
    POSTGRES_PORT: int #= 5432

    # Slack
    SLACK_BOT_TOKEN: str #= ""
    SLACK_APP_TOKEN: str #= ""
    SLACK_SIGNING_SECRET: str #= ""

    # n8n
    N8N_WEBHOOK_URL: str #= ""

    @property
    def connection_string(self) -> str:
        """Connection string used by SQLAlchemy and PGVector."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_settings() -> Settings:
    """Cached so the .env file is parsed only once per process."""
    return Settings()


settings = get_settings()
