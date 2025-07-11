# AI-Q Unified Container Setup

This document describes the unified container architecture for the AI-Q Knowledge Library System, where all application services run within a single containerized environment.

## Architecture Overview

The AI-Q system uses a unified container approach with the following components:

### Main Application Container (`ai-q-app`)
- **Python FastAPI Server**: Main API server handling knowledge management operations
- **Next.js Web Dashboard**: React-based frontend for user interaction
- **Cadvisor**: Container monitoring and metrics collection
- **Supervisor**: Process management for multiple services

### Infrastructure Services (External)
- **PostgreSQL**: Primary relational database
- **Redis**: Caching and session storage
- **Elasticsearch**: Full-text search and indexing
- **Neo4j**: Graph database for knowledge relationships
- **Weaviate**: Vector database for semantic search
- **MinIO**: Object storage for files and media
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Visualization and dashboards

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 8GB RAM available
- 20GB free disk space

### 1. Start the Unified System

```bash
# Start all services
docker-compose -f docker-compose.unified.yml up -d

# View logs
docker-compose -f docker-compose.unified.yml logs -f ai-q-app

# Check service status
docker-compose -f docker-compose.unified.yml ps
```

### 2. Access Services

Once all services are running, you can access:

- **Web Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health
- **Container Monitoring**: http://localhost:8081
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **Neo4j Browser**: http://localhost:7474 (neo4j/password)

## Configuration

### Environment Variables

The system uses environment variables for configuration. Create a `.env` file in the project root:

```env
# Application Settings
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=3000
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# Database Settings
POSTGRES_DB=aiq_knowledge
POSTGRES_USER=aiq_user
POSTGRES_PASSWORD=aiq_password
POSTGRES_PORT=5432

# Redis Settings
REDIS_PASSWORD=your-redis-password

# Elasticsearch Settings
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=elastic

# Neo4j Settings
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# MinIO Settings
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# Feature Flags
ENABLE_RAG=true
ENABLE_GRAPH_DB=true
ENABLE_VECTOR_DB=true
ENABLE_MONITORING=true
```

### Service Dependencies

The unified container waits for all infrastructure services to be ready before starting the application services:

1. **PostgreSQL**: Database connectivity
2. **Redis**: Cache connectivity
3. **Elasticsearch**: Search service
4. **Neo4j**: Graph database
5. **Weaviate**: Vector database
6. **MinIO**: Object storage

## Development Workflow

### Local Development

For local development, you can run the infrastructure services with Docker and the application locally:

```bash
# Start only infrastructure services
docker-compose -f docker-compose.infrastructure.yml up -d

# Run API server locally
python src/main.py

# Run web dashboard locally
cd src/web
npm install
npm run dev
```

### Building the Unified Container

```bash
# Build the unified container
docker build -f Dockerfile.unified -t ai-q-unified .

# Run the unified container
docker run -p 8000:8000 -p 3000:3000 -p 8081:8080 ai-q-unified
```

## Monitoring and Logs

### Container Logs

```bash
# View all logs
docker-compose -f docker-compose.unified.yml logs

# View specific service logs
docker-compose -f docker-compose.unified.yml logs ai-q-app
docker-compose -f docker-compose.unified.yml logs postgres
```

### Health Checks

The system includes health checks for all services:

- **API Server**: `GET /health`
- **Web Dashboard**: `GET /api/health`
- **Infrastructure Services**: Docker health checks

### Metrics and Monitoring

- **Cadvisor**: Container resource usage (http://localhost:8081)
- **Prometheus**: Metrics collection (http://localhost:9090)
- **Grafana**: Dashboards (http://localhost:3001)

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 3000, 8000, 8081, 5432, 6379, 9200, 7474, 7687, 8080, 9000, 9001, 9090, 3001 are available

2. **Memory Issues**: Increase Docker memory allocation to at least 8GB

3. **Service Startup Failures**: Check logs for specific service errors:
   ```bash
   docker-compose -f docker-compose.unified.yml logs [service-name]
   ```

4. **Database Connection Issues**: Ensure PostgreSQL and other databases are fully started before the application container

### Debug Mode

Enable debug mode by setting environment variables:

```env
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Reset and Cleanup

```bash
# Stop all services
docker-compose -f docker-compose.unified.yml down

# Remove volumes (WARNING: This will delete all data)
docker-compose -f docker-compose.unified.yml down -v

# Rebuild containers
docker-compose -f docker-compose.unified.yml build --no-cache
```

## Security Considerations

1. **Change Default Passwords**: Update all default passwords in production
2. **Network Security**: Use Docker networks to isolate services
3. **Environment Variables**: Store sensitive data in environment variables
4. **SSL/TLS**: Configure HTTPS for production deployments
5. **Access Control**: Implement proper authentication and authorization

## Production Deployment

For production deployment:

1. Use environment-specific configuration files
2. Set up proper SSL/TLS certificates
3. Configure backup strategies for databases
4. Set up monitoring and alerting
5. Use secrets management for sensitive data
6. Configure proper resource limits and scaling

## Support

For issues and questions:

1. Check the logs: `docker-compose -f docker-compose.unified.yml logs`
2. Verify service health: `docker-compose -f docker-compose.unified.yml ps`
3. Check resource usage: `docker stats`
4. Review configuration files and environment variables 