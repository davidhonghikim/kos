#!/usr/bin/env python3
"""
kOS Environment Generator from Centralized Configuration
Generates all environment variables from centralized_ports.json
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def load_centralized_config():
    """Load the centralized ports configuration"""
    config_path = Path(__file__).parent.parent / "config" / "centralized_ports.json"
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_path} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing {config_path}: {e}")
        sys.exit(1)

def generate_env_variables(config):
    """Generate environment variables from centralized config"""
    env_vars = {}
    
    # Add metadata
    env_vars.update({
        "KOS_CONFIG_VERSION": config["metadata"]["version"],
        "KOS_CONFIG_LAST_UPDATED": config["metadata"]["last_updated"]
    })
    
    # Add missing Docker environment variables
    env_vars.update({
        # Core Docker variables
        "KOS_ENVIRONMENT": "development",
        "KOS_DEBUG": "true",
        "KOS_LOG_LEVEL": "info",
        
        # API and host configuration - CRITICAL for Docker
        "KOS_API_HOST": "localhost",
        "KOS_API_PORT": "8000",
        "KOS_API_CONTAINER_PORT": "8000",
        "KOS_POSTGRES_HOST": "localhost",
        "KOS_GITEA_DOMAIN": "localhost",
        "KOS_OLLAMA_HOST": "localhost",
        "KOS_OLLAMA_ORIGINS": "*",
        
        # Protocol specifications for centralized_ports.json references
        "KOS_BACKEND_PROTOCOL": "http",
        "KOS_FRONTEND_PROTOCOL": "http",
        "KOS_NGINX_PROTOCOL": "http",
        "KOS_BACKEND_HEALTH_CHECK": "/health",
        
        # Image specifications
        "KOS_NGINX_IMAGE": "nginx:alpine",
        "KOS_POSTGRES_IMAGE": "postgres:15-alpine",
        "KOS_REDIS_IMAGE": "redis:7-alpine",
        "KOS_NEO4J_IMAGE": "neo4j:5.15",
        "KOS_GITEA_IMAGE": "gitea/gitea:latest",
        "KOS_OPENWEBUI_IMAGE": "ghcr.io/open-webui/open-webui:main",
        "KOS_OLLAMA_IMAGE": "ollama/ollama:latest",
        "KOS_VAULT_IMAGE": "vault:latest",
        "KOS_SUPABASE_IMAGE": "supabase/postgres:15.1.0.117",
        "KOS_BROWSERUSE_IMAGE": "browseruse/browseruse:latest",
        "KOS_CONTEXT7_IMAGE": "context7/context7:latest",
        "KOS_CODIUM_IMAGE": "codium/codium:latest",
        "KOS_ELASTICSEARCH_IMAGE": "elasticsearch:8.11.0",
        "KOS_WEAVIATE_IMAGE": "semitechnologies/weaviate:1.22.4",
        "KOS_MINIO_IMAGE": "minio/minio:latest",
        "KOS_PROMETHEUS_IMAGE": "prom/prometheus:latest",
        "KOS_GRAFANA_IMAGE": "grafana/grafana:latest",
        
        # Security and authentication - NO SECRETS/KEYS
        "KOS_VAULT_ROOT_TOKEN": "",
        "KOS_OPENWEBUI_SECRET_KEY": "",
        "KOS_OPENWEBUI_DEFAULT_MODELS": "",
        "KOS_GRAFANA_ADMIN_PASSWORD": "",
        
        # Service-specific configuration - NO PASSWORDS
        "KOS_GITEA_DB_NAME": "gitea",
        "KOS_GITEA_DB_USER": "gitea",
        "KOS_GITEA_DB_PASSWORD": "",
        "KOS_SUPABASE_DB_PASSWORD": "",
        "KOS_SUPABASE_JWT_SECRET": "",
        "KOS_SUPABASE_ANON_KEY": "",
        "KOS_SUPABASE_SERVICE_ROLE_KEY": "",
        "KOS_BROWSERUSE_API_KEY": "",
        "KOS_BROWSERUSE_WORKSPACE": "/app/workspace",
        "KOS_CONTEXT7_API_KEY": "",
        "KOS_CONTEXT7_DATABASE_URL": "postgresql://admin@kos-postgres:5432/context7",
        "KOS_CODIUM_EXTENSIONS": "ms-vscode.vscode-typescript-next,github.copilot",
        "KOS_CODIUM_SETTINGS": "{}",
        "KOS_CODIUM_COPILOT_ENABLED": "false",
        "KOS_PROMPT_MANAGER_DB_URL": "postgresql://admin@kos-postgres:5432/prompt_manager",
        "KOS_PROMPT_MANAGER_REDIS_URL": "redis://kos-redis:6379/0",
        "KOS_PROMPT_MANAGER_API_KEY": "",
        "KOS_ARTIFACT_MANAGER_DB_URL": "postgresql://admin@kos-postgres:5432/artifact_manager",
        "KOS_ARTIFACT_MANAGER_STORAGE_PATH": "/app/storage",
        "KOS_ARTIFACT_MANAGER_MAX_FILE_SIZE": "100MB",
        "KOS_ARTIFACT_MANAGER_API_KEY": "",
        "KOS_MINIO_ROOT_USER": "",
        "KOS_MINIO_ROOT_PASSWORD": ""
    })
    
    # Add network config
    env_vars.update({
        "KOS_DEFAULT_HOST": config["network_config"]["default_host"],
        "KOS_CONTAINER_NETWORK": config["network_config"]["container_network"],
        "KOS_INTERNAL_DOMAIN": config["network_config"]["internal_domain"]
    })
    
    # Define actual port values (matching docker-compose.yml expectations)
    port_values = {
        # Core services - Docker Legacy Format
        "KOS_API_PORT": "8000",                    # docker-compose.yml expects this
        "KOS_API_CONTAINER_PORT": "8000",          # docker-compose.yml expects this
        "KOS_API_HOST": "localhost",               # docker-compose.yml expects this
        "KOS_FRONTEND_PORT": "3000",               # docker-compose.yml expects this
        "KOS_FRONTEND_CONTAINER_PORT": "3000",     # docker-compose.yml expects this
        "KOS_NGINX_PORT": "80",                    # docker-compose.yml expects this
        "KOS_NGINX_CONTAINER_PORT": "80",          # docker-compose.yml expects this
        
        # Also include modern format for docker/compose/ files
        "KOS_BACKEND_EXTERNAL_PORT": "8000",
        "KOS_BACKEND_INTERNAL_PORT": "8000",
        "KOS_FRONTEND_EXTERNAL_PORT": "3000",
        "KOS_FRONTEND_INTERNAL_PORT": "3000",
        "KOS_NGINX_EXTERNAL_PORT": "80",
        "KOS_NGINX_INTERNAL_PORT": "80",
        
        # Databases - Docker Legacy Format
        "KOS_POSTGRES_PORT": "5432",
        "KOS_POSTGRES_CONTAINER_PORT": "5432",
        "KOS_REDIS_PORT": "6379", 
        "KOS_REDIS_CONTAINER_PORT": "6379",
        "KOS_NEO4J_PORT": "7687",
        "KOS_NEO4J_CONTAINER_PORT": "7687",
        "KOS_NEO4J_HTTP_PORT": "7474",
        "KOS_NEO4J_HTTP_CONTAINER_PORT": "7474",
        
        # Also include modern format
        "KOS_POSTGRES_EXTERNAL_PORT": "5432",
        "KOS_POSTGRES_INTERNAL_PORT": "5432",
        "KOS_REDIS_EXTERNAL_PORT": "6379",
        "KOS_REDIS_INTERNAL_PORT": "6379",
        "KOS_NEO4J_EXTERNAL_PORT": "7687",
        "KOS_NEO4J_INTERNAL_PORT": "7687",
        "KOS_NEO4J_HTTP_EXTERNAL_PORT": "7474",
        "KOS_NEO4J_HTTP_INTERNAL_PORT": "7474",
        
        # Development services - Docker Legacy Format
        "KOS_GITEA_PORT": "3002",
        "KOS_GITEA_CONTAINER_PORT": "3000",
        "KOS_GITEA_SSH_PORT": "2222",
        "KOS_GITEA_SSH_CONTAINER_PORT": "22",
        "KOS_OPENWEBUI_PORT": "3001",
        "KOS_OPENWEBUI_CONTAINER_PORT": "8080",
        "KOS_OLLAMA_PORT": "11434",
        "KOS_OLLAMA_CONTAINER_PORT": "11434",
        
        # Also include modern format
        "KOS_GITEA_EXTERNAL_PORT": "3002",
        "KOS_GITEA_INTERNAL_PORT": "3000",
        "KOS_GITEA_SSH_EXTERNAL_PORT": "2222",
        "KOS_GITEA_SSH_INTERNAL_PORT": "22",
        "KOS_OPENWEBUI_EXTERNAL_PORT": "3001",
        "KOS_OPENWEBUI_INTERNAL_PORT": "8080",
        "KOS_OLLAMA_EXTERNAL_PORT": "11434",
        "KOS_OLLAMA_INTERNAL_PORT": "11434",
        # Additional Development Services - Docker Legacy Format  
        "KOS_SUPABASE_PORT": "54321",
        "KOS_SUPABASE_CONTAINER_PORT": "5432",
        "KOS_SUPABASE_STUDIO_PORT": "3003",
        "KOS_SUPABASE_STUDIO_CONTAINER_PORT": "3000",
        "KOS_BROWSERUSE_PORT": "3004",
        "KOS_BROWSERUSE_CONTAINER_PORT": "3000",
        "KOS_CONTEXT7_PORT": "3005",
        "KOS_CONTEXT7_CONTAINER_PORT": "3000",
        "KOS_CODIUM_PORT": "3006",
        "KOS_CODIUM_CONTAINER_PORT": "8080",
        
        # Also include modern format
        "KOS_SUPABASE_EXTERNAL_PORT": "54321",
        "KOS_SUPABASE_INTERNAL_PORT": "5432",
        "KOS_SUPABASE_STUDIO_EXTERNAL_PORT": "3003",
        "KOS_SUPABASE_STUDIO_INTERNAL_PORT": "3000",
        "KOS_BROWSERUSE_EXTERNAL_PORT": "3004",
        "KOS_BROWSERUSE_INTERNAL_PORT": "3000",
        "KOS_CONTEXT7_EXTERNAL_PORT": "3005",
        "KOS_CONTEXT7_INTERNAL_PORT": "3000",
        "KOS_CODIUM_EXTERNAL_PORT": "3006",
        "KOS_CODIUM_INTERNAL_PORT": "8080",
        
        # Monitoring services - Docker Legacy Format
        "KOS_PROMETHEUS_PORT": "9090",
        "KOS_PROMETHEUS_CONTAINER_PORT": "9090",
        "KOS_GRAFANA_PORT": "3007",
        "KOS_GRAFANA_CONTAINER_PORT": "3000",
        
        # Also include modern format
        "KOS_PROMETHEUS_EXTERNAL_PORT": "9090",
        "KOS_PROMETHEUS_INTERNAL_PORT": "9090",
        "KOS_GRAFANA_EXTERNAL_PORT": "3007",
        "KOS_GRAFANA_INTERNAL_PORT": "3000",
        
        # Storage services - Docker Legacy Format
        "KOS_ELASTICSEARCH_PORT": "9200",
        "KOS_ELASTICSEARCH_CONTAINER_PORT": "9200",
        "KOS_WEAVIATE_PORT": "8082",
        "KOS_WEAVIATE_CONTAINER_PORT": "8080",
        "KOS_MINIO_PORT": "9000",
        "KOS_MINIO_CONTAINER_PORT": "9000",
        "KOS_MINIO_CONSOLE_PORT": "9001",
        "KOS_MINIO_CONSOLE_CONTAINER_PORT": "9001",
        
        # Also include modern format
        "KOS_ELASTICSEARCH_EXTERNAL_PORT": "9200",
        "KOS_ELASTICSEARCH_INTERNAL_PORT": "9200",
        "KOS_WEAVIATE_EXTERNAL_PORT": "8082",
        "KOS_WEAVIATE_INTERNAL_PORT": "8080",
        "KOS_MINIO_EXTERNAL_PORT": "9000",
        "KOS_MINIO_INTERNAL_PORT": "9000",
        "KOS_MINIO_CONSOLE_EXTERNAL_PORT": "9001",
        "KOS_MINIO_CONSOLE_INTERNAL_PORT": "9001",
        
        # Security services - Docker Legacy Format
        "KOS_VAULT_PORT": "8200",
        "KOS_VAULT_CONTAINER_PORT": "8200",
        
        # Manager services - Docker Legacy Format
        "KOS_PROMPT_MANAGER_PORT": "3008",
        "KOS_PROMPT_MANAGER_CONTAINER_PORT": "8000",
        "KOS_ARTIFACT_MANAGER_PORT": "3009",
        "KOS_ARTIFACT_MANAGER_CONTAINER_PORT": "8000",
        
        # Also include modern format
        "KOS_VAULT_EXTERNAL_PORT": "8200",
        "KOS_VAULT_INTERNAL_PORT": "8200",
        "KOS_PROMPT_MANAGER_EXTERNAL_PORT": "3008",
        "KOS_PROMPT_MANAGER_INTERNAL_PORT": "8000",
        "KOS_ARTIFACT_MANAGER_EXTERNAL_PORT": "3009",
        "KOS_ARTIFACT_MANAGER_INTERNAL_PORT": "8000"
    }
    
    # Define host values
    host_values = {
        "KOS_BACKEND_HOST": "localhost",
        "KOS_BACKEND_CONTAINER_HOST": "kos-backend",
        "KOS_FRONTEND_HOST": "localhost",
        "KOS_FRONTEND_CONTAINER_HOST": "kos-frontend",
        "KOS_NGINX_HOST": "localhost",
        "KOS_NGINX_CONTAINER_HOST": "kos-nginx",
        "KOS_POSTGRES_HOST": "localhost",
        "KOS_POSTGRES_CONTAINER_HOST": "kos-postgres",
        "KOS_REDIS_HOST": "localhost",
        "KOS_REDIS_CONTAINER_HOST": "kos-redis",
        "KOS_NEO4J_HOST": "localhost",
        "KOS_NEO4J_CONTAINER_HOST": "kos-neo4j",
        "KOS_GITEA_HOST": "localhost",
        "KOS_GITEA_CONTAINER_HOST": "kos-gitea",
        "KOS_OPENWEBUI_HOST": "localhost",
        "KOS_OPENWEBUI_CONTAINER_HOST": "kos-openwebui",
        "KOS_OLLAMA_HOST": "localhost",
        "KOS_OLLAMA_CONTAINER_HOST": "kos-ollama",
        "KOS_SUPABASE_HOST": "localhost",
        "KOS_SUPABASE_CONTAINER_HOST": "kos-supabase",
        "KOS_BROWSERUSE_HOST": "localhost",
        "KOS_BROWSERUSE_CONTAINER_HOST": "kos-browseruse",
        "KOS_CONTEXT7_HOST": "localhost",
        "KOS_CONTEXT7_CONTAINER_HOST": "kos-context7",
        "KOS_CODIUM_HOST": "localhost",
        "KOS_CODIUM_CONTAINER_HOST": "kos-codium",
        "KOS_PROMETHEUS_HOST": "localhost",
        "KOS_PROMETHEUS_CONTAINER_HOST": "kos-prometheus",
        "KOS_GRAFANA_HOST": "localhost",
        "KOS_GRAFANA_CONTAINER_HOST": "kos-grafana",
        "KOS_ELASTICSEARCH_HOST": "localhost",
        "KOS_ELASTICSEARCH_CONTAINER_HOST": "kos-elasticsearch",
        "KOS_WEAVIATE_HOST": "localhost",
        "KOS_WEAVIATE_CONTAINER_HOST": "kos-weaviate",
        "KOS_MINIO_HOST": "localhost",
        "KOS_MINIO_CONTAINER_HOST": "kos-minio",
        "KOS_VAULT_HOST": "localhost",
        "KOS_VAULT_CONTAINER_HOST": "kos-vault",
        "KOS_PROMPT_MANAGER_HOST": "localhost",
        "KOS_PROMPT_MANAGER_CONTAINER_HOST": "kos-prompt-manager",
        "KOS_ARTIFACT_MANAGER_HOST": "localhost",
        "KOS_ARTIFACT_MANAGER_CONTAINER_HOST": "kos-artifact-manager"
    }
    
    # Add all port and host values
    env_vars.update(port_values)
    env_vars.update(host_values)
    
    # Generate service environment variables from config
    for category, services in config["services"].items():
        for service_name, service_config in services.items():
            # Convert service name to environment variable prefix
            prefix = service_name.upper().replace("-", "_")
            
            # Add protocol and description - resolve variable references
            if "protocol" in service_config:
                protocol_value = service_config["protocol"]
                # Resolve any variable references like ${KOS_BACKEND_PROTOCOL} to actual values
                if protocol_value.startswith("${") and protocol_value.endswith("}"):
                    var_name = protocol_value[2:-1]  # Extract variable name
                    protocol_value = env_vars.get(var_name, "http")  # Default to http
                env_vars[f"{prefix}_PROTOCOL"] = protocol_value
            if "description" in service_config:
                env_vars[f"{prefix}_DESCRIPTION"] = service_config["description"]
            
            # Handle additional ports (SSH, HTTP, console, etc.)
            for key, value in service_config.items():
                if key.endswith("_port") and key != "external_port" and key != "internal_port":
                    env_key = f"{prefix}_{key.upper()}"
                    env_vars[env_key] = str(value)
                elif key.endswith("_internal_port") and key != "internal_port":
                    env_key = f"{prefix}_{key.upper()}"
                    env_vars[env_key] = str(value)
            
            # Handle database-specific configurations
            if "default_db" in service_config:
                env_vars[f"{prefix}_DB"] = service_config["default_db"]
            if "default_user" in service_config:
                env_vars[f"{prefix}_USER"] = service_config["default_user"]
            if "default_password" in service_config:
                env_vars[f"{prefix}_PASSWORD"] = service_config["default_password"]
    
    # Generate Docker image variables
    for service_name, image in config["docker_images"].items():
        prefix = service_name.upper().replace("-", "_")
        env_vars[f"{prefix}_IMAGE"] = image
    
    # Add environment variables from config
    for category, vars_dict in config["environment_variables"].items():
        for key, value in vars_dict.items():
            env_vars[key] = value
    
    return env_vars

def generate_service_enable_flags(config):
    """Generate service enable flags"""
    enable_flags = {}
    
    for category, services in config["services"].items():
        for service_name in services.keys():
            prefix = service_name.upper().replace("-", "_")
            enable_flags[f"KOS_ENABLE_{prefix}"] = "true"
    
    return enable_flags

def write_env_file(env_vars, output_path, template_path=None):
    """Write environment variables to file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("# =============================================================================\n")
        f.write("# kOS Environment Variables - Auto-generated from centralized_ports.json\n")
        f.write("# =============================================================================\n")
        f.write("# DO NOT EDIT THIS FILE DIRECTLY - Edit config/centralized_ports.json instead\n")
        f.write("# Generated on: {}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        f.write("# =============================================================================\n\n")
        
        # Group variables by category
        categories = {
            "NETWORK": [k for k in env_vars.keys() if k.startswith("KOS_DEFAULT_") or k.startswith("KOS_CONTAINER_") or k.startswith("KOS_INTERNAL_")],
            "CORE_SERVICES": [k for k in env_vars.keys() if "KOS_BACKEND" in k or "KOS_FRONTEND" in k or "KOS_NGINX" in k],
            "DATABASES": [k for k in env_vars.keys() if "KOS_POSTGRES" in k or "KOS_REDIS" in k or "KOS_NEO4J" in k],
            "DEVELOPMENT": [k for k in env_vars.keys() if any(x in k for x in ["KOS_GITEA", "KOS_OPENWEBUI", "KOS_OLLAMA", "KOS_SUPABASE", "KOS_BROWSERUSE", "KOS_CONTEXT7", "KOS_CODIUM"])],
            "MONITORING": [k for k in env_vars.keys() if "KOS_PROMETHEUS" in k or "KOS_GRAFANA" in k],
            "STORAGE": [k for k in env_vars.keys() if "KOS_ELASTICSEARCH" in k or "KOS_WEAVIATE" in k or "KOS_MINIO" in k],
            "SECURITY": [k for k in env_vars.keys() if "KOS_VAULT" in k],
            "MANAGERS": [k for k in env_vars.keys() if "KOS_PROMPT_MANAGER" in k or "KOS_ARTIFACT_MANAGER" in k],
            "DOCKER_IMAGES": [k for k in env_vars.keys() if k.endswith("_IMAGE")],
            "ENVIRONMENT": [k for k in env_vars.keys() if k.startswith("KOS_ENVIRONMENT") or k.startswith("KOS_DEBUG") or k.startswith("KOS_LOG_")],
            "SECURITY_CONFIG": [k for k in env_vars.keys() if k.startswith("KOS_JWT_") or k.startswith("KOS_BCRYPT_")],
            "CORS": [k for k in env_vars.keys() if k.startswith("KOS_CORS_")],
            "CONFIG": [k for k in env_vars.keys() if k.startswith("KOS_CONFIG_")]
        }
        
        for category, variables in categories.items():
            if variables:
                f.write(f"\n# =============================================================================\n")
                f.write(f"# {category}\n")
                f.write(f"# =============================================================================\n")
                for var in sorted(variables):
                    f.write(f"{var}={env_vars[var]}\n")

def main():
    """Main function"""
    print("Loading centralized configuration...")
    config = load_centralized_config()
    
    print("Generating environment variables...")
    env_vars = generate_env_variables(config)
    enable_flags = generate_service_enable_flags(config)
    
    # Merge enable flags
    env_vars.update(enable_flags)
    
    # Write to env directory
    env_dir = Path(__file__).parent.parent / "env"
    env_dir.mkdir(exist_ok=True)
    
    # Generate local.env.generated (TEST FILE - SAFE)
    local_env_path = env_dir / "local.env.generated"
    write_env_file(env_vars, local_env_path)
    print(f"Generated: {local_env_path}")
    
    # Generate settings.env.generated with enable flags (TEST FILE - SAFE)
    settings_env_path = env_dir / "settings.env.generated"
    write_env_file(enable_flags, settings_env_path)
    print(f"Generated: {settings_env_path}")
    
    # Generate .env file for Docker Compose to use automatically
    docker_env_path = Path(__file__).parent.parent / ".env"
    write_env_file(env_vars, docker_env_path)
    print(f"Generated: {docker_env_path}")
    print("\nDocker Compose will now automatically load variables from .env file!")
    
    # Create a summary of all ports
    print("\n" + "="*80)
    print("PORT SUMMARY")
    print("="*80)
    for category, services in config["services"].items():
        print(f"\n{category.upper()}:")
        for service_name, service_config in services.items():
            print(f"  {service_name}: {service_config['external_port']} -> {service_config['internal_port']}")
    
    print(f"\nTotal services: {sum(len(services) for services in config['services'].values())}")
    print(f"Total environment variables generated: {len(env_vars)}")
    print("\nConfiguration files updated successfully!")

if __name__ == "__main__":
    main() 