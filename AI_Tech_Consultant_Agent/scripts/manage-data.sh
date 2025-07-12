#!/bin/bash

# AI Tech Consultant Agent - Data Management Script
# This script helps manage data in the .docker directory

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

# Function to show data directory sizes
show_sizes() {
    print_status "Data directory sizes:"
    echo ""
    
    if [[ -d ".docker" ]]; then
        du -sh .docker/* 2>/dev/null || print_warning "No data directories found"
    else
        print_warning ".docker directory does not exist"
    fi
    
    echo ""
    print_status "Total .docker directory size:"
    du -sh .docker 2>/dev/null || print_warning ".docker directory does not exist"
}

# Function to backup data
backup_data() {
    local backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
    
    print_status "Creating backup in $backup_dir..."
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    # Stop services before backup
    print_status "Stopping services for backup..."
    docker-compose down
    
    # Copy data directories
    if [[ -d ".docker" ]]; then
        cp -r .docker "$backup_dir/"
        print_success "Backup created successfully in $backup_dir"
    else
        print_warning "No .docker directory to backup"
    fi
    
    # Restart services
    print_status "Restarting services..."
    docker-compose up -d
}

# Function to restore data
restore_data() {
    local backup_dir="$1"
    
    if [[ -z "$backup_dir" ]]; then
        print_error "Please specify backup directory"
        echo "Usage: $0 restore <backup-directory>"
        exit 1
    fi
    
    if [[ ! -d "$backup_dir" ]]; then
        print_error "Backup directory $backup_dir does not exist"
        exit 1
    fi
    
    print_status "Restoring data from $backup_dir..."
    
    # Stop services before restore
    print_status "Stopping services for restore..."
    docker-compose down
    
    # Remove existing data
    if [[ -d ".docker" ]]; then
        rm -rf .docker
    fi
    
    # Restore from backup
    cp -r "$backup_dir/.docker" .
    print_success "Data restored successfully from $backup_dir"
    
    # Restart services
    print_status "Restarting services..."
    docker-compose up -d
}

# Function to clean data
clean_data() {
    print_warning "This will permanently delete all data in .docker directory!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Stopping services..."
        docker-compose down
        
        print_status "Cleaning data directories..."
        rm -rf .docker/mem0/*
        rm -rf .docker/postgres/*
        rm -rf .docker/redis/*
        
        print_success "Data cleaned successfully"
        
        print_status "Restarting services..."
        docker-compose up -d
    else
        print_status "Clean operation cancelled"
    fi
}

# Function to list backups
list_backups() {
    if [[ -d "backups" ]]; then
        print_status "Available backups:"
        ls -la backups/
    else
        print_warning "No backups directory found"
    fi
}

# Function to inspect data
inspect_data() {
    print_status "Inspecting .docker directory structure:"
    echo ""
    
    if [[ -d ".docker" ]]; then
        tree .docker -a || ls -la .docker/
    else
        print_warning ".docker directory does not exist"
    fi
    
    echo ""
    print_status "Checking service data:"
    
    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_success "Services are running"
        
        # Show recent logs
        echo ""
        print_status "Recent service logs:"
        docker-compose logs --tail=10
    else
        print_warning "Services are not running"
    fi
}

# Function to show help
show_help() {
    echo "AI Tech Consultant Agent - Data Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  sizes     Show data directory sizes"
    echo "  backup    Create a backup of all data"
    echo "  restore   Restore data from backup"
    echo "  clean     Clean all data (WARNING: destructive)"
    echo "  list      List available backups"
    echo "  inspect   Inspect data structure and services"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 sizes"
    echo "  $0 backup"
    echo "  $0 restore backups/20231201_143022"
    echo "  $0 inspect"
}

# Main script logic
case "${1:-help}" in
    "sizes")
        show_sizes
        ;;
    "backup")
        backup_data
        ;;
    "restore")
        restore_data $2
        ;;
    "clean")
        clean_data
        ;;
    "list")
        list_backups
        ;;
    "inspect")
        inspect_data
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