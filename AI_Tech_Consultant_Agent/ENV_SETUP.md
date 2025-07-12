# Environment Variables Setup

## Required Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Google API Keys
GOOGLE_API_KEY=your-google-api-key-here

# OpenAI API Key (for LiteLLM)
OPENAI_API_KEY=your-openai-api-key-here

# Mem0 Configuration
# Get your API key from https://mem0.ai
MEM0_API_KEY=your-mem0-api-key-here
MEM0_ENV=development
MEM0_HOST=http://localhost:8080

# Langfuse Configuration
# Get your keys from https://cloud.langfuse.com
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key-here
LANGFUSE_SECRET_KEY=your-langfuse-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# OpenTelemetry (optional)
OTEL_EXPORTER_OTLP_ENDPOINT=
OTEL_EXPORTER_OTLP_HEADERS=

# LiteLLM Configuration (optional)
LITELLM_API_BASE=

# General Settings
ENV=development
DEBUG=true
```

## Getting API Keys

### Mem0 API Key
1. Go to https://mem0.ai
2. Sign up or log in
3. Navigate to your API settings
4. Copy your API key

### Langfuse Keys
1. Go to https://cloud.langfuse.com
2. Create an account or log in
3. Create a new project
4. Go to project settings
5. Copy the public and secret keys

### Google API Key
1. Go to Google Cloud Console
2. Enable the Generative AI API
3. Create credentials (API key)

### OpenAI API Key
1. Go to https://platform.openai.com
2. Sign up or log in
3. Go to API keys section
4. Create a new API key

## Running with Docker Compose

If you're using Docker Compose, you can also set environment variables in the `env.docker.example` file and rename it to `env.docker`.

### Local Development Setup

For local development with Docker Compose:

```bash
# Start Mem0 and other services
./scripts/start-services.sh start

# Set environment variables for local development
MEM0_ENV=development
MEM0_HOST=http://localhost:8080
```

### Cloud Setup

For cloud deployment:

```bash
# Set environment variables for cloud
MEM0_ENV=production
MEM0_HOST=https://api.mem0.ai  # or your cloud Mem0 endpoint
```

## Troubleshooting

- If you see "Mem0 not configured" messages, make sure your `MEM0_API_KEY` is set correctly
- If you see "Mem0 server not running" errors, ensure Docker services are started with `./scripts/start-services.sh start`
- If you see "LangFuse environment variables not fully set", ensure all LangFuse variables are configured
- The system will fall back to mock implementations if services are not available 