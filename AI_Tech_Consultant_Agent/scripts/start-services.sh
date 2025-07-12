#!/bin/bash

# AI Tech Consultant Agent - Service Management Script
# This script manages the Docker Compose services for Mem0 and Langfuse

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to check if ports are available
check_ports() {
    local ports=("8080" "3000" "5432" "6379")
    local services=("Mem0" "Langfuse" "PostgreSQL" "Redis")
    
    for i in "${!ports[@]}"; do
        if lsof -i :${ports[$i]} > /dev/null 2>&1; then
            print_warning "Port ${ports[$i]} (${services[$i]}) is already in use"
        else
            print_success "Port ${ports[$i]} (${services[$i]}) is available"
        fi
    done
}

# Function to start services
start_services() {
    print_status "Starting Docker Compose services..."
    
    # Ensure .docker directories exist
    print_status "Creating data directories..."
    mkdir -p .docker/{mem0,postgres,redis}
    
    # Set proper permissions for data directories
    print_status "Setting directory permissions..."
    chmod 755 .docker
    chmod 755 .docker/mem0
    chmod 755 .docker/postgres
    chmod 755 .docker/redis
    
    # Pull latest images
    print_status "Pulling latest images..."
    docker-compose pull
    
    # Start services in detached mode
    print_status "Starting services..."
    docker-compose up -d
    
    print_success "Services started successfully!"
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    # Wait for services to be ready
    sleep 10
    
    # Check each service
    local services=("mem0" "postgres" "redis" "langfuse")
    local endpoints=("http://localhost:8080/health" "N/A" "N/A" "http://localhost:3000/api/health")
    local ports=("8080" "5432" "6379" "3000")
    
    for i in "${!services[@]}"; do
        local service=${services[$i]}
        local port=${ports[$i]}
        
        if docker-compose ps $service | grep -q "Up"; then
            print_success "$service is running on port $port"
            
            # Check HTTP endpoints if available
            if [[ "${endpoints[$i]}" != "N/A" ]]; then
                if curl -f -s "${endpoints[$i]}" > /dev/null 2>&1; then
                    print_success "$service health check passed"
                else
                    print_warning "$service health check failed (may still be starting up)"
                fi
            fi
        else
            print_error "$service is not running"
        fi
    done
}

# Function to show service URLs
show_urls() {
    echo ""
    print_status "Service URLs:"
    echo "  Mem0:      http://localhost:8080"
    echo "  Langfuse:  http://localhost:3000"
    echo "  PostgreSQL: localhost:5432"
    echo "  Redis:     localhost:6379"
    echo ""
    print_status "You can now run your AI Tech Consultant Agent application!"
}

# Function to stop services
stop_services() {
    print_status "Stopping Docker Compose services..."
    docker-compose down
    print_success "Services stopped successfully!"
}

# Function to show logs
show_logs() {
    local service=${1:-""}
    if [[ -n "$service" ]]; then
        print_status "Showing logs for $service..."
        docker-compose logs -f $service
    else
        print_status "Showing logs for all services..."
        docker-compose logs -f
    fi
}

# Function to show status
show_status() {
    print_status "Service status:"
    docker-compose ps
}

# Function to show help
show_help() {
    echo "AI Tech Consultant Agent - Service Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start all services"
    echo "  stop      Stop all services"
    echo "  restart   Restart all services"
    echo "  status    Show service status"
    echo "  logs      Show logs (all services or specific service)"
    echo "  health    Check service health"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs mem0"
    echo "  $0 status"
}

# Main script logic
case "${1:-start}" in
    "start")
        check_docker
        check_docker_compose
        check_ports
        start_services
        check_health
        show_urls
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        sleep 2
        check_docker
        check_docker_compose
        start_services
        check_health
        show_urls
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs $2
        ;;
    "health")
        check_health
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 