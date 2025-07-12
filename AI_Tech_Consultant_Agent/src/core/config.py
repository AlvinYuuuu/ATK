"""
Core configuration setup, client initializations, and environment variable loading.
"""

import os
import base64
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Load environment variables from .env file
load_dotenv()

def setup_mem0():
    """Initialize Mem0 configuration."""
    return True
    try:
        MEM0_API_KEY = os.environ.get("MEM0_API_KEY")
        MEM0_ENV = os.environ.get("MEM0_ENV", "production")
        MEM0_HOST = os.environ.get("MEM0_HOST")
        
        if not MEM0_API_KEY:
            print("⚠️ MEM0_API_KEY not set. Mem0 will not be available.")
            return False
        
        # Set Mem0 environment variables
        os.environ["MEM0_API_KEY"] = MEM0_API_KEY
        os.environ["MEM0_ENV"] = MEM0_ENV
        
        # Configure Mem0 host
        if MEM0_HOST:
            os.environ["MEM0_HOST"] = MEM0_HOST
            print(f"✅ Mem0 configured successfully (env: {MEM0_ENV}, host: {MEM0_HOST})")
        else:
            # Default to localhost if running with Docker Compose
            if MEM0_ENV == "development":
                os.environ["MEM0_HOST"] = "http://localhost:8080"
                print(f"✅ Mem0 configured for local development (host: http://localhost:8080)")
            else:
                print(f"✅ Mem0 configured for cloud (env: {MEM0_ENV})")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to configure Mem0: {e}")
        return False

def setup_langfuse_tracing():
    """Initializes LangFuse tracing via OpenTelemetry for ADK compatibility."""
    try:
        LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY")
        LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY")
        LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST")

        if not all([LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST]):
            print("LangFuse environment variables not fully set. Tracing will be disabled.")
            return

        # Encode credentials for the OTLP header
        auth_header = base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

        # Configure the OTel exporter to send data to LangFuse
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{LANGFUSE_HOST}/api/public/otel"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_header}"

        # Set up the TracerProvider
        provider = TracerProvider(
            resource=Resource.create({"service.name": "ai-tech-consultant-agent"})
        )

        # Configure the OTLPSpanExporter
        exporter = OTLPSpanExporter()

        # Add the BatchSpanProcessor to the provider
        provider.add_span_processor(BatchSpanProcessor(exporter))

        # Set the global TracerProvider
        trace.set_tracer_provider(provider)
        print("LangFuse tracing initialized successfully.")

    except Exception as e:
        print(f"Failed to initialize LangFuse tracing: {e}")

# Initialize Mem0 configuration
MEM0_AVAILABLE = setup_mem0()

# Initialize tracing when this module is loaded
setup_langfuse_tracing()

# Initialize LiteLLM for model routing
import litellm

# Set up LiteLLM configuration
litellm.api_key = os.environ.get("GOOGLE_API_KEY")  # Default to OpenAI
litellm.api_base = os.environ.get("LITELLM_API_BASE")

# Configure model routing for different tasks
LITELLM_CONFIG = {
    "complex_reasoning": "gpt-4",  # For complex analysis and strategy
    "text_generation": "gpt-3.5-turbo",  # For general text generation
    "summarization": "claude-3-haiku",  # For summarization tasks
    "code_generation": "gpt-4"  # For code and technical content
}
