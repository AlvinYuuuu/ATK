# Docker Compose Setup for AI Tech Consultant Agent

This document describes how to set up and run the required services (Mem0 and Langfuse) using Docker Compose.

## Services Overview

The `docker-compose.yml` file includes the following services:

1. **Mem0** - Vector database for AI memory management
2. **Langfuse** - LLM observability and tracing platform
3. **PostgreSQL** - Database for Langfuse
4. **Redis** - Caching layer for Langfuse (optional)

## Quick Start

1. **Start all services:**
   ```bash
   docker-compose up -d
   ```

2. **Check service status:**
   ```bash
   docker-compose ps
   ```

3. **View logs:**
   ```bash
   docker-compose logs -f [service-name]
   ```

4. **Stop services:**
   ```bash
   docker-compose down
   ```

## Service Details

### Mem0 (Port 8080)
- **URL:** http://localhost:8080
- **Purpose:** Vector database for storing and retrieving AI agent memories
- **Health Check:** http://localhost:8080/health

### Langfuse (Port 3000)
- **URL:** http://localhost:3000
- **Purpose:** LLM observability, tracing, and analytics
- **Health Check:** http://localhost:3000/api/health

### PostgreSQL (Port 5432)
- **Database:** langfuse
- **User:** langfuse
- **Password:** langfuse
- **Purpose:** Persistent storage for Langfuse data

### Redis (Port 6379)
- **Purpose:** Caching layer for Langfuse
- **Health Check:** Redis PING command

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Langfuse Configuration
LANGFUSE_SECRET_KEY=your-secret-key-here
LANGFUSE_PUBLIC_KEY=your-public-key-here
LANGFUSE_HOST=http://localhost:3000

# Mem0 Configuration
MEM0_HOST=http://localhost:8080
MEM0_API_KEY=your-mem0-api-key-here

# PostgreSQL Configuration
POSTGRES_DB=langfuse
POSTGRES_USER=langfuse
POSTGRES_PASSWORD=langfuse

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Application Configuration
NEXTAUTH_SECRET=your-nextauth-secret-here
NEXTAUTH_URL=http://localhost:3000
```

## Data Persistence

Data is persisted in the `.docker` directory within the project:

- `.docker/mem0/` - Mem0 vector database data
- `.docker/postgres/` - PostgreSQL database data  
- `.docker/redis/` - Redis cache data

This local mounting approach provides several benefits:
- Easy access to data for debugging and backup
- Data persists between container restarts
- No need to manage Docker volumes externally
- Data is organized within the project structure

## Network Configuration

All services run on the `ai-consultant-network` Docker network for secure inter-service communication.

## Health Checks

Each service includes health checks to ensure proper startup order and service availability:

- **Mem0:** HTTP health check on `/health` endpoint
- **Langfuse:** HTTP health check on `/api/health` endpoint
- **PostgreSQL:** Database connectivity check
- **Redis:** PING command check

## Troubleshooting

### Service Won't Start
1. Check if ports are already in use:
   ```bash
   lsof -i :8080  # Mem0
   lsof -i :3000  # Langfuse
   lsof -i :5432  # PostgreSQL
   lsof -i :6379  # Redis
   ```

2. View service logs:
   ```bash
   docker-compose logs [service-name]
   ```

### Data Persistence Issues
1. Check local data directories:
   ```bash
   ls -la .docker/
   ```

2. Check data directory permissions:
   ```bash
   ls -la .docker/mem0/
   ls -la .docker/postgres/
   ls -la .docker/redis/
   ```

3. If containers can't write to directories, fix permissions:
   ```bash
   sudo chown -R 1000:1000 .docker/mem0/
   sudo chown -R 999:999 .docker/postgres/
   sudo chown -R 1001:1001 .docker/redis/
   ```

### Network Issues
1. Check network connectivity:
   ```bash
   docker network ls
   docker network inspect ai-consultant-network
   ```

## Security Notes

- Change default passwords in production
- Use strong secrets for NEXTAUTH_SECRET and API keys
- Consider using Docker secrets for sensitive data
- Restrict network access in production environments

## Production Considerations

For production deployment:

1. Use external databases instead of containerized PostgreSQL
2. Implement proper backup strategies
3. Use reverse proxy (nginx/traefik) for SSL termination
4. Set up monitoring and alerting
5. Use Docker secrets for sensitive configuration
6. Implement proper logging and log rotation 