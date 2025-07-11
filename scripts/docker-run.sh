#!/bin/bash

# AI-Q Docker Runner Script
# Provides easy access to Docker commands from the project root

set -e

# Default values
COMPOSE_FILE="unified"
SERVICE=""
BUILD=false
FOLLOW=false

# Define compose file paths
declare -A COMPOSE_FILES=(
    ["unified"]="docker/compose/docker-compose.unified.yml"
    ["development"]="docker/compose/docker-compose.yml"
    ["infrastructure"]="docker/compose/docker-compose.infrastructure.yml"
    ["feature-flags"]="docker/compose/docker-compose.feature-flags.yml"
)

show_help() {
    echo "AI-Q Docker Runner"
    echo ""
    echo "Usage:"
    echo "  ./scripts/docker-run.sh up [compose-file] [options]"
    echo "  ./scripts/docker-run.sh down [compose-file]"
    echo "  ./scripts/docker-run.sh logs [compose-file] [service] [-f]"
    echo "  ./scripts/docker-run.sh build [compose-file]"
    echo "  ./scripts/docker-run.sh status [compose-file]"
    echo ""
    echo "Compose Files:"
    echo "  unified        - Unified container setup (default)"
    echo "  development    - Development setup with all services"
    echo "  infrastructure - Infrastructure services only"
    echo "  feature-flags  - Generated based on feature flags"
    echo ""
    echo "Examples:"
    echo "  ./scripts/docker-run.sh up unified"
    echo "  ./scripts/docker-run.sh logs unified ai-q-app -f"
    echo "  ./scripts/docker-run.sh build feature-flags"
}

run_docker_compose() {
    local action="$1"
    local service="$2"
    
    local docker_cmd="docker-compose -f $COMPOSE_PATH $action"
    
    if [[ -n "$service" ]]; then
        docker_cmd="$docker_cmd $service"
    fi
    
    echo "Running: $docker_cmd"
    eval "$docker_cmd"
}

# Parse command line arguments
COMMAND=""
while [[ $# -gt 0 ]]; do
    case $1 in
        up|down|logs|build|status|restart|stop|start|help)
            COMMAND="$1"
            shift
            ;;
        unified|development|infrastructure|feature-flags)
            COMPOSE_FILE="$1"
            shift
            ;;
        --build|-b)
            BUILD=true
            shift
            ;;
        -f|--follow)
            FOLLOW=true
            shift
            ;;
        -*)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
        *)
            if [[ -z "$SERVICE" ]]; then
                SERVICE="$1"
            else
                echo "Unknown argument: $1"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate compose file selection
if [[ ! -v COMPOSE_FILES[$COMPOSE_FILE] ]]; then
    echo "Error: Invalid compose file '$COMPOSE_FILE'"
    echo "Available options: ${!COMPOSE_FILES[@]}"
    exit 1
fi

COMPOSE_PATH="${COMPOSE_FILES[$COMPOSE_FILE]}"

# Check if compose file exists
if [[ ! -f "$COMPOSE_PATH" ]]; then
    echo "Error: Compose file not found: $COMPOSE_PATH"
    exit 1
fi

# Main command logic
case $COMMAND in
    up)
        if [[ "$BUILD" == true ]]; then
            run_docker_compose "up --build -d" "$SERVICE"
        else
            run_docker_compose "up -d" "$SERVICE"
        fi
        ;;
    down)
        run_docker_compose "down"
        ;;
    logs)
        local log_cmd="logs"
        if [[ "$FOLLOW" == true ]]; then
            log_cmd="$log_cmd -f"
        fi
        run_docker_compose "$log_cmd" "$SERVICE"
        ;;
    build)
        run_docker_compose "build" "$SERVICE"
        ;;
    status)
        run_docker_compose "ps"
        ;;
    restart)
        run_docker_compose "restart" "$SERVICE"
        ;;
    stop)
        run_docker_compose "stop" "$SERVICE"
        ;;
    start)
        run_docker_compose "start" "$SERVICE"
        ;;
    help)
        show_help
        ;;
    "")
        echo "Error: No command specified"
        show_help
        exit 1
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'"
        show_help
        exit 1
        ;;
esac 