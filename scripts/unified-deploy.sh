#!/bin/bash

# ============================================================================
# AI-Q Unified Deployment Script
# ============================================================================
# This script deploys the complete ai-Q system with all services
# ============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
COMPOSE_DIR="$PROJECT_ROOT/docker/compose"
ENV_FILE="$COMPOSE_DIR/.env"
ENV_TEMPLATE="$COMPOSE_DIR/env.template"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Docker
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "System requirements check passed"
}

# Function to setup environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_TEMPLATE" ]; then
            cp "$ENV_TEMPLATE" "$ENV_FILE"
            print_success "Environment file created from template"
            print_warning "Please review and modify $ENV_FILE before deployment"
        else
            print_error "Environment template not found at $ENV_TEMPLATE"
            exit 1
        fi
    else
        print_status "Environment file already exists"
    fi
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create data directories
    sudo mkdir -p /opt/ai-q/data/{openwebui,ollama,gitea,nextcloud,postgresql,redis,elasticsearch,neo4j,weaviate,minio,grafana,prometheus,registry}
    
    # Create config directories
    sudo mkdir -p /opt/ai-q/config/{gitea,nextcloud,admin-panel,nginx,ssl,grafana,prometheus}
    
    # Create log directories
    sudo mkdir -p /opt/ai-q/logs
    
    # Create backup directories
    sudo mkdir -p /opt/ai-q/backups
    
    # Set proper permissions
    sudo chown -R 1000:1000 /opt/ai-q/data
    sudo chown -R 1000:1000 /opt/ai-q/config
    sudo chown -R 1000:1000 /opt/ai-q/logs
    sudo chown -R 1000:1000 /opt/ai-q/backups
    
    print_success "Directories created successfully"
}

# Function to validate configuration
validate_configuration() {
    print_status "Validating configuration..."
    
    # Check if environment file exists
    if [ ! -f "$ENV_FILE" ]; then
        print_error "Environment file not found. Please run setup first."
        exit 1
    fi
    
    # Validate Docker Compose file
    cd "$COMPOSE_DIR"
    if docker-compose -f unified.yml config >/dev/null 2>&1; then
        print_success "Docker Compose configuration is valid"
    else
        print_error "Docker Compose configuration is invalid"
        docker-compose -f unified.yml config
        exit 1
    fi
}

# Function to deploy services
deploy_services() {
    print_status "Deploying ai-Q services..."
    
    cd "$COMPOSE_DIR"
    
    # Pull latest images
    print_status "Pulling latest Docker images..."
    docker-compose -f unified.yml pull
    
    # Start services
    print_status "Starting services..."
    docker-compose -f unified.yml up -d
    
    print_success "Services deployment initiated"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Checking service health (attempt $attempt/$max_attempts)..."
        
        # Check if all services are running
        if docker-compose -f "$COMPOSE_DIR/unified.yml" ps | grep -q "Up"; then
            local unhealthy_services=$(docker-compose -f "$COMPOSE_DIR/unified.yml" ps | grep -v "Up" | wc -l)
            if [ "$unhealthy_services" -eq 0 ]; then
                print_success "All services are running and healthy"
                return 0
            fi
        fi
        
        sleep 10
        attempt=$((attempt + 1))
    done
    
    print_warning "Some services may still be starting up. Check logs for details."
}

# Function to display service status
show_status() {
    print_status "Service Status:"
    cd "$COMPOSE_DIR"
    docker-compose -f unified.yml ps
    
    echo ""
    print_status "Service URLs:"
    echo "  - AI-Q Web Dashboard: http://localhost:3000"
    echo "  - AI-Q API: http://localhost:8000"
    echo "  - OpenWebUI: http://localhost:11001"
    echo "  - Gitea: http://localhost:3002"
    echo "  - NextCloud: http://localhost:8080"
    echo "  - Admin Panel: http://localhost:9000"
    echo "  - MinIO Console: http://localhost:9001"
    echo "  - Grafana: http://localhost:3001"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - cAdvisor: http://localhost:8081"
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    cd "$COMPOSE_DIR"
    docker-compose -f unified.yml logs -f
}

# Function to stop services
stop_services() {
    print_status "Stopping ai-Q services..."
    cd "$COMPOSE_DIR"
    docker-compose -f unified.yml down
    print_success "Services stopped"
}

# Function to restart services
restart_services() {
    print_status "Restarting ai-Q services..."
    cd "$COMPOSE_DIR"
    docker-compose -f unified.yml restart
    print_success "Services restarted"
}

# Function to clean up
cleanup() {
    print_status "Cleaning up..."
    cd "$COMPOSE_DIR"
    docker-compose -f unified.yml down -v
    print_success "Cleanup completed"
}

# Function to show help
show_help() {
    echo "AI-Q Unified Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy      - Deploy all services (default)"
    echo "  setup       - Setup environment and directories"
    echo "  start       - Start all services"
    echo "  stop        - Stop all services"
    echo "  restart     - Restart all services"
    echo "  status      - Show service status"
    echo "  logs        - Show service logs"
    echo "  cleanup     - Stop and remove all containers and volumes"
    echo "  help        - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Deploy all services"
    echo "  $0 status    # Show current status"
    echo "  $0 logs      # Show service logs"
}

# Main execution
main() {
    local command="${1:-deploy}"
    
    case "$command" in
        "deploy")
            check_requirements
            setup_environment
            create_directories
            validate_configuration
            deploy_services
            wait_for_services
            show_status
            ;;
        "setup")
            check_requirements
            setup_environment
            create_directories
            ;;
        "start")
            deploy_services
            wait_for_services
            show_status
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            restart_services
            wait_for_services
            show_status
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@" 