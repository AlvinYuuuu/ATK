"""
Core configuration setup, client initializations, and settings management.
"""

import os
import base64
import litellm
from typing import Optional
from langfuse import get_client

from pydantic import model_validator, PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Load environment variables from .env file, allowing for override.
load_dotenv(override=True)


class Settings(BaseSettings):
    """
    Manages application settings using Pydantic, loading from environment variables.
    """
    # Mem0 Configuration
    MEM0_API_KEY: Optional[str] = None
    MEM0_API_BASE: Optional[str] = None # For self-hosted instances

    # -- Mem0 Self-Hosted Configuration --
    # LLM
    MEM0_LLM_PROVIDER: str = "litellm"
    MEM0_LLM_MODEL: str = "vertex_ai/gemini-2.5-flash"
    MEM0_LLM_TEMPERATURE: float = 0.2
    MEM0_LLM_MAX_TOKENS: int = 20000

    # Vector Store
    MEM0_VECTOR_STORE_PROVIDER: str = "chroma"
    MEM0_VECTOR_STORE_COLLECTION_NAME: str = "atk"
    MEM0_VECTOR_STORE_HOST: str = "http://localhost:8001"

    # Embedder
    MEM0_EMBEDDER_PROVIDER: str = "ollama"
    MEM0_EMBEDDER_MODEL: str = "dengcao/Qwen3-Embedding-0.6B:F16"
    MEM0_EMBEDDER_OLLAMA_BASE_URL: str = "http://localhost:11434"

    # --- Database Configuration ---
    # Assembled from individual components if not provided directly.
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "atk_agent_db"
    
    # The final database connection string.
    # Can be set directly in .env or will be assembled from the parts above.
    DATABASE_URL: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def assemble_db_connection(cls, v: dict) -> dict:
        """Assembles the database connection string from parts if not provided."""
        if isinstance(v, dict) and 'DATABASE_URL' not in v:
            # Build the base URL using Pydantic for validation of parts
            base_url = str(PostgresDsn.build(
                scheme="postgresql",
                username=v.get('POSTGRES_USER', cls.model_fields['POSTGRES_USER'].default),
                password=v.get('POSTGRES_PASSWORD', cls.model_fields['POSTGRES_PASSWORD'].default),
                host=v.get('POSTGRES_HOST', cls.model_fields['POSTGRES_HOST'].default),
                port=int(v.get('POSTGRES_PORT', cls.model_fields['POSTGRES_PORT'].default)),
                path=v.get('POSTGRES_DB', cls.model_fields['POSTGRES_DB'].default),
            ))
            # Inject the psycopg2 driver into the URL for SQLAlchemy compatibility
            v['DATABASE_URL'] = base_url.replace("postgresql://", "postgresql+psycopg2://")
        return v

    # Langfuse Configuration
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

# Create a single, reusable settings instance
settings = Settings()


def setup_langfuse_tracing():
    """Initializes LangFuse tracing using settings from the Settings object."""
    if not all([settings.LANGFUSE_PUBLIC_KEY, settings.LANGFUSE_SECRET_KEY]):
        print("LangFuse environment variables not fully set. Tracing will be disabled.")
        return

    try:
        # Encode credentials for the OTLP header
        auth_header = base64.b64encode(
            f"{settings.LANGFUSE_PUBLIC_KEY}:{settings.LANGFUSE_SECRET_KEY}".encode()
        ).decode()

        # Configure the OTel exporter to send data to LangFuse
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{settings.LANGFUSE_HOST}/api/public/otel"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_header}"

        langfuse = get_client()
 
        # Verify connection
        if langfuse.auth_check():
            print("Langfuse client is authenticated and ready!")
        else:
            print("Authentication failed. Please check your credentials and host.")
            
        print("LangFuse tracing initialized successfully.")

    except Exception as e:
        print(f"Failed to initialize LangFuse tracing: {e}")


# Initialize services when this module is loaded
setup_langfuse_tracing()
