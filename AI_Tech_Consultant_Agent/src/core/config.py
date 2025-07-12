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

# Initialize tracing when this module is loaded
setup_langfuse_tracing()

# You can add other client initializations here, e.g., for Mem0 or LiteLLM
# mem0_client = ...
# litellm.api_key = ...
