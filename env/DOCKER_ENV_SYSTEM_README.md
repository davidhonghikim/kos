# kOS Environment Variable System - Complete Guide

## Overview

The kOS environment variable system is a comprehensive, organized configuration management solution that eliminates hardcoded values throughout the entire system. This document explains how the system works and how different components use it.

## System Architecture

### File Organization

```
kos/env/
├── README.md                           # Main environment system guide
├── DOCKER_ENV_SYSTEM_README.md        # This file - Docker integration guide
├── ports.env.example                   # All ports, IPs, container names, service names
├── local.env.example                   # Local service configuration
├── cloud.env.example                   # Cloud service configuration  
├── api-keys.env.example               # API keys and secrets
├── settings.env.example               # System settings and feature flags
├── ai-q.env.example                   # AI-Q specific configuration
├── settings/                          # Additional configuration files
└── [user override files]              # local.env, cloud.env, etc. (not in git)
```

### Loading Priority

The system loads environment files in this order (later files override earlier ones):

1. `env/local.env.example` - Base local configuration
2. `env/cloud.env.example` - Base cloud configuration  
3. `env/api-keys.env.example` - Base API keys structure
4. `env/settings.env.example` - Base system settings
5. `env/local.env` - Your local overrides
6. `env/cloud.env` - Your cloud overrides
7. `env/api-keys.env` - Your actual API keys
8. `env/settings.env` - Your system settings

## Core Principles

### 1. NO HARDCODED VALUES
- **All configuration** comes from environment variables
- **No hardcoded ports, IPs, passwords, or paths** anywhere in the codebase
- **Docker files** use `${VARIABLE_NAME}` syntax
- **Application code** reads from environment variables

### 2. Service-First Organization
- **Each service** has its own section with all related variables
- **Variables are grouped** by functionality (enable/disable, host, port, credentials, etc.)
- **Clear separation** between core services and optional services

### 3. Centralized Management
- **All ports** defined in `ports.env.example`
- **All container names** defined in `ports.env.example`
- **All service names** defined in `ports.env.example`
- **All network configuration** defined in `ports.env.example`

## How Docker Uses the Environment System

### Docker Compose Integration

Docker Compose files use environment variables in several ways:

#### 1. Container Names
```yaml
# Before (hardcoded)
container_name: ai-q-postgres

# After (environment variable)
container_name: ${KOS_POSTGRES_CONTAINER_NAME}
```

#### 2. Port Mappings
```yaml
# Before (hardcoded)
ports:
  - "5432:5432"

# After (environment variable)
ports:
  - "${KOS_POSTGRES_EXTERNAL_PORT}:${KOS_POSTGRES_INTERNAL_PORT}"
```

#### 3. Network Configuration
```yaml
# Before (hardcoded)
networks:
  - ai-q-network

# After (environment variable)
networks:
  - ${KOS_CONTAINER_NETWORK}
```

#### 4. Environment Variables
```yaml
# Before (hardcoded)
environment:
  POSTGRES_DB: aiq_knowledge
  POSTGRES_USER: aiq_user
  POSTGRES_PASSWORD: aiq_password

# After (environment variable)
environment:
  POSTGRES_DB: ${KOS_POSTGRES_DB}
  POSTGRES_USER: ${KOS_POSTGRES_USER}
  POSTGRES_PASSWORD: ${KOS_POSTGRES_PASSWORD}
```

#### 5. Image and Version
```yaml
# Before (hardcoded)
image: postgres:15-alpine

# After (environment variable)
image: ${KOS_POSTGRES_IMAGE}:${KOS_POSTGRES_VERSION}
```

#### 6. Volumes
```yaml
# Before (hardcoded)
volumes:
  - postgres_data:/var/lib/postgresql/data

# After (environment variable)
volumes:
  - ${KOS_POSTGRES_VOLUME}:/var/lib/postgresql/data
```

### Docker Environment File Loading

Docker Compose automatically loads environment files:

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    env_file:
      - ../env/local.env.example
      - ../env/ports.env.example
      - ../env/local.env  # User overrides
```

## How Services Use the Environment System

### 1. Service Enable/Disable
```bash
# Environment variable controls service startup
KOS_POSTGRES_ENABLE=true
KOS_REDIS_ENABLE=true
KOS_ELASTICSEARCH_ENABLE=false
```

### 2. Service Configuration
```bash
# Database configuration
KOS_POSTGRES_HOST=postgres
KOS_POSTGRES_PORT=5432
KOS_POSTGRES_DB=kos_db
KOS_POSTGRES_USER=kos-admin
KOS_POSTGRES_PASSWORD=kos-30437

# Redis configuration
KOS_REDIS_HOST=redis
KOS_REDIS_PORT=6379
KOS_REDIS_PASSWORD=kos-30437
```

### 3. Feature Flags
```bash
# Enable/disable features
KOS_ENABLE_RAG=true
KOS_ENABLE_GRAPH_DB=true
KOS_ENABLE_VECTOR_DB=true
KOS_ENABLE_MONITORING=true
```

## Environment Variable Categories

### 1. Network Configuration (`ports.env.example`)
```bash
# Network settings
KOS_DEFAULT_HOST=localhost
KOS_CONTAINER_NETWORK=kos-network
KOS_NETWORK_SUBNET=172.20.0.0/16

# Container names
KOS_POSTGRES_CONTAINER_NAME=kos-postgres
KOS_REDIS_CONTAINER_NAME=kos-redis

# Service names
KOS_POSTGRES_SERVICE_NAME=postgres
KOS_REDIS_SERVICE_NAME=redis

# Port mappings
KOS_POSTGRES_EXTERNAL_PORT=5432
KOS_POSTGRES_INTERNAL_PORT=5432
```

### 2. Service Configuration (`local.env.example`)
```bash
# Service enable/disable
KOS_POSTGRES_ENABLE=true
KOS_REDIS_ENABLE=true

# Service credentials
KOS_ADMIN_USER=kos-admin
KOS_ADMIN_PASSWORD=kos-30437

# Service-specific settings
KOS_POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
KOS_REDIS_COMMAND=redis-server --appendonly yes
```

### 3. Docker Configuration (`local.env.example`)
```bash
# Docker images and versions
KOS_POSTGRES_IMAGE=postgres
KOS_POSTGRES_VERSION=15-alpine

# Docker volumes
KOS_POSTGRES_VOLUME=kos-postgres-data
KOS_REDIS_VOLUME=kos-redis-data

# Health check configuration
KOS_HEALTH_CHECK_INTERVAL=30s
KOS_HEALTH_CHECK_TIMEOUT=10s
KOS_HEALTH_CHECK_RETRIES=3

# File paths
KOS_SRC_PATH=../../src
KOS_CONFIG_PATH=../../config
```

## Usage Examples

### 1. Starting Services with Environment Variables

```bash
# Load environment and start services
export $(cat env/local.env.example env/ports.env.example | xargs)
docker-compose up -d
```

### 2. Overriding Default Values

```bash
# In your local.env file
KOS_POSTGRES_PORT=5433  # Override default port
KOS_ADMIN_PASSWORD=my-secure-password  # Override default password
```

### 3. Conditional Service Startup

```bash
# Enable only specific services
KOS_POSTGRES_ENABLE=true
KOS_REDIS_ENABLE=true
KOS_ELASTICSEARCH_ENABLE=false
KOS_NEO4J_ENABLE=false

# Start only enabled services
docker-compose up -d
```

### 4. Environment-Specific Configuration

```bash
# Development
KOS_ENVIRONMENT=development
KOS_DEBUG=true
KOS_LOG_LEVEL=debug

# Production
KOS_ENVIRONMENT=production
KOS_DEBUG=false
KOS_LOG_LEVEL=info
```

## Best Practices

### 1. Variable Naming
- **Use `KOS_` prefix** for all kOS-specific variables
- **Use descriptive names** that indicate the service and purpose
- **Use consistent naming patterns** across all services

### 2. Default Values
- **Provide sensible defaults** in example files
- **Use `${VARIABLE:-default}` syntax** for fallback values
- **Document all variables** with clear descriptions

### 3. Security
- **Never commit** actual passwords or API keys
- **Use example files** for structure, actual files for values
- **Rotate secrets** regularly
- **Use strong passwords** for admin accounts

### 4. Organization
- **Group related variables** together
- **Use clear section headers** with comments
- **Maintain consistent ordering** across files
- **Update documentation** when adding new variables

## Troubleshooting

### Common Issues

#### 1. Environment Variables Not Loading
```bash
# Check if environment file exists
ls -la env/local.env

# Check if variables are set
echo $KOS_POSTGRES_ENABLE

# Load environment manually
source env/local.env
```

#### 2. Docker Compose Not Using Variables
```bash
# Check if env_file is specified in docker-compose.yml
# Ensure environment files are in the correct path
# Verify variable syntax: ${VARIABLE_NAME}
```

#### 3. Port Conflicts
```bash
# Check what's using a port
netstat -tulpn | grep :5432

# Change port in environment file
KOS_POSTGRES_EXTERNAL_PORT=5433
```

#### 4. Service Not Starting
```bash
# Check if service is enabled
echo $KOS_POSTGRES_ENABLE

# Check Docker logs
docker-compose logs postgres

# Verify environment variables are set
docker-compose config
```

## Migration Guide

### From Hardcoded to Environment Variables

#### Step 1: Identify Hardcoded Values
```bash
# Search for hardcoded values
grep -r "5432\|6379\|localhost\|password" docker/
```

#### Step 2: Add Environment Variables
```bash
# Add to appropriate environment file
echo "KOS_POSTGRES_PORT=5432" >> env/ports.env.example
```

#### Step 3: Update Docker Files
```yaml
# Replace hardcoded values with variables
ports:
  - "${KOS_POSTGRES_PORT}:5432"
```

#### Step 4: Test Configuration
```bash
# Verify environment loading
docker-compose config

# Test service startup
docker-compose up -d postgres
```

## Advanced Configuration

### 1. Multiple Environments
```bash
# Development
cp env/local.env.example env/local.dev.env

# Staging
cp env/local.env.example env/local.staging.env

# Production
cp env/local.env.example env/local.prod.env
```

### 2. Service Profiles
```bash
# Core services only
KOS_CORE_SERVICES=true
KOS_AI_SERVICES=false
KOS_MONITORING_SERVICES=false

# Full stack
KOS_CORE_SERVICES=true
KOS_AI_SERVICES=true
KOS_MONITORING_SERVICES=true
```

### 3. Dynamic Configuration
```bash
# Use environment variables to set other variables
KOS_API_URL=http://${KOS_DEFAULT_HOST}:${KOS_API_EXTERNAL_PORT}
KOS_DATABASE_URL=postgresql://${KOS_POSTGRES_USER}:${KOS_POSTGRES_PASSWORD}@${KOS_POSTGRES_HOST}:${KOS_POSTGRES_PORT}/${KOS_POSTGRES_DB}
```

## Conclusion

The kOS environment variable system provides a robust, flexible, and secure way to manage configuration across all components. By following the principles outlined in this guide, you can maintain a clean, maintainable, and scalable system that eliminates hardcoded values and provides clear separation of concerns.

For more information, see the main environment system guide in `README.md`. 