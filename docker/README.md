# AI-Q Docker Organization

## Overview

This directory contains all Docker-related files for the AI-Q project, organized for clarity and maintainability.

## Directory Structure

```
docker/
├── README.md                    # This file
├── README-UNIFIED.md           # Original unified setup documentation
├── compose/                     # Docker Compose configurations
│   ├── docker-compose.yml      # Main development setup
│   ├── docker-compose.unified.yml # Unified container setup
│   ├── docker-compose.infrastructure.yml # Infrastructure only
│   └── docker-compose.json     # JSON format configuration
├── dockerfiles/                 # Dockerfile definitions
│   ├── Dockerfile.unified      # Unified application container
│   ├── Dockerfile.api          # API-only container
│   └── Dockerfile.web          # Web-only container
└── config/                      # Docker-specific configurations
    ├── supervisor/             # Supervisor configurations
    ├── prometheus/             # Prometheus configurations
    └── grafana/                # Grafana configurations
```

## Quick Start

### Development Setup
```bash
# Start with all services
docker-compose -f docker/compose/docker-compose.yml up -d

# Start with feature flags
docker-compose -f docker/compose/docker-compose.feature-flags.yml up -d
```

### Production Setup
```bash
# Unified container (recommended)
docker-compose -f docker/compose/docker-compose.unified.yml up -d

# Infrastructure only
docker-compose -f docker/compose/docker-compose.infrastructure.yml up -d
```

## Configuration Files

### Docker Compose Files

1. **docker-compose.yml** - Main development setup with all services
2. **docker-compose.unified.yml** - Single container with all services
3. **docker-compose.infrastructure.yml** - Infrastructure services only
4. **docker-compose.feature-flags.yml** - Generated based on feature flags

### Dockerfiles

1. **Dockerfile.unified** - Multi-service container with API and web
2. **Dockerfile.api** - API server only
3. **Dockerfile.web** - Web dashboard only

## Feature Flag Integration

The Docker setup integrates with the feature flag system:

```bash
# Generate Docker Compose based on feature flags
python3 scripts/feature-flag-parser.py generate-compose

# The generated file will be: docker/compose/docker-compose.feature-flags.yml
```

## Service Ports

| Service | Port | Description |
|---------|------|-------------|
| API Server | 8000 | FastAPI backend |
| Web Dashboard | 3000 | Next.js frontend |
| PostgreSQL | 5432 | Database |
| Redis | 6379 | Cache |
| Elasticsearch | 9200 | Search |
| Neo4j | 7474 | Graph database |
| Weaviate | 8080 | Vector database |
| MinIO | 9000/9001 | Object storage |
| Prometheus | 9090 | Metrics |
| Grafana | 3001 | Monitoring |

## Environment Variables

Create a `.env` file in the project root:

```env
# Application
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=3000

# Database
POSTGRES_DB=aiq_knowledge
POSTGRES_USER=aiq_user
POSTGRES_PASSWORD=aiq_password

# Feature Flags
ENABLE_RAG=true
ENABLE_GRAPH_DB=true
ENABLE_VECTOR_DB=true
ENABLE_MONITORING=true
```

## Building Images

### Unified Container
```bash
docker build -f docker/dockerfiles/Dockerfile.unified -t ai-q:unified .
```

### Individual Services
```bash
# API only
docker build -f docker/dockerfiles/Dockerfile.api -t ai-q:api .

# Web only
docker build -f docker/dockerfiles/Dockerfile.web -t ai-q:web .
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Check if ports are already in use
   - Modify ports in docker-compose files

2. **Service Dependencies**
   - Ensure all required services are enabled
   - Check feature flag configuration

3. **Memory Issues**
   - Reduce Elasticsearch memory: `ES_JAVA_OPTS=-Xms256m -Xmx512m`
   - Disable unused services via feature flags

### Logs and Debugging

```bash
# View all logs
docker-compose -f docker/compose/docker-compose.unified.yml logs

# View specific service logs
docker-compose -f docker/compose/docker-compose.unified.yml logs ai-q-app

# Follow logs
docker-compose -f docker/compose/docker-compose.unified.yml logs -f
```

## Migration from Root Directory

If you have Docker files in the root directory:

```bash
# Move to organized structure
mv docker-compose*.yml docker/compose/
mv Dockerfile* docker/dockerfiles/
mv README-UNIFIED.md docker/
```

## Best Practices

1. **Use Feature Flags**: Enable only needed services
2. **Environment Separation**: Different configs for dev/prod
3. **Resource Limits**: Set appropriate memory/CPU limits
4. **Health Checks**: All services have health checks
5. **Logging**: Centralized logging configuration
6. **Security**: Use secrets for sensitive data

## Contributing

When adding new Docker configurations:

1. Place files in appropriate subdirectories
2. Update this README with new services
3. Add health checks for new services
4. Update feature flag integration if needed
5. Test with different feature combinations 