#!/usr/bin/env python3
"""
kOS Docker Compose Updater
Updates docker-compose.yml to use only environment variables from centralized config
"""

import json
import os
import sys
from pathlib import Path
import re

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

def generate_docker_compose_template(config):
    """Generate docker-compose.yml template using only environment variables"""
    
    template = """version: '3.8'

# =============================================================================
# kOS Docker Compose Configuration
# =============================================================================
# All ports, IPs, and configurations are managed via environment variables
# Edit config/centralized_ports.json to change any settings
# =============================================================================

services:
"""
    
    # Generate services from centralized config
    for category, services in config["services"].items():
        template += f"\n  # {category.upper()} SERVICES\n"
        
        for service_name, service_config in services.items():
            # Service header
            template += f"\n  # {service_config['description']}\n"
            template += f"  {service_name}:\n"
            
            # Image
            if service_name in config["docker_images"]:
                template += f"    image: ${{{service_name.upper().replace('-', '_')}_IMAGE}}\n"
            else:
                template += f"    build:\n"
                template += f"      context: .\n"
                template += f"      dockerfile: docker/{service_name.replace('kos-', '')}.Dockerfile\n"
            
            # Container name
            template += f"    container_name: {service_name}\n"
            
            # Ports
            template += f"    ports:\n"
            template += f"      - \"${{{service_name.upper().replace('-', '_')}_EXTERNAL_PORT}}:${{{service_name.upper().replace('-', '_')}_INTERNAL_PORT}}\"\n"
            
            # Additional ports (SSH, HTTP, console, etc.)
            for key, value in service_config.items():
                if key.endswith("_port") and key != "external_port" and key != "internal_port":
                    env_key = f"{service_name.upper().replace('-', '_')}_{key.upper()}"
                    template += f"      - \"${{{env_key}}}:${{{env_key.replace('_PORT', '_INTERNAL_PORT')}}}\"\n"
            
            # Environment variables
            template += f"    environment:\n"
            
            # Service-specific environment variables
            if service_name == "kos-postgres":
                template += f"      - POSTGRES_DB=${{{service_name.upper().replace('-', '_')}_DB}}\n"
                template += f"      - POSTGRES_USER=${{{service_name.upper().replace('-', '_')}_USER}}\n"
                template += f"      - POSTGRES_PASSWORD=${{{service_name.upper().replace('-', '_')}_PASSWORD}}\n"
            elif service_name == "kos-redis":
                template += f"      - REDIS_PASSWORD=${{{service_name.upper().replace('-', '_')}_PASSWORD}}\n"
                template += f"      - REDIS_DB=${{{service_name.upper().replace('-', '_')}_DB}}\n"
            elif service_name == "kos-neo4j":
                template += f"      - NEO4J_AUTH=${{{service_name.upper().replace('-', '_')}_USER}}/${{{service_name.upper().replace('-', '_')}_PASSWORD}}\n"
                template += f"      - NEO4J_PLUGINS='[\"apoc\"]'\n"
            elif service_name == "kos-gitea":
                template += f"      - GITEA__database__DB_TYPE=postgres\n"
                template += f"      - GITEA__database__HOST=${{KOS_POSTGRES_HOST}}:${{KOS_POSTGRES_EXTERNAL_PORT}}\n"
                template += f"      - GITEA__database__NAME=${{KOS_GITEA_DB}}\n"
                template += f"      - GITEA__database__USER=${{KOS_GITEA_USER}}\n"
                template += f"      - GITEA__database__PASSWD=${{KOS_GITEA_PASSWORD}}\n"
                template += f"      - GITEA__server__DOMAIN=${{KOS_GITEA_HOST}}\n"
                template += f"      - GITEA__server__ROOT_URL=http://${{KOS_GITEA_HOST}}:${{KOS_GITEA_EXTERNAL_PORT}}/\n"
            elif service_name == "kos-openwebui":
                template += f"      - OLLAMA_BASE_URL=http://${{KOS_OLLAMA_HOST}}:${{KOS_OLLAMA_EXTERNAL_PORT}}\n"
                template += f"      - WEBUI_SECRET_KEY=${{KOS_OPENWEBUI_SECRET_KEY}}\n"
                template += f"      - DEFAULT_MODELS=${{KOS_OPENWEBUI_DEFAULT_MODELS}}\n"
            elif service_name == "kos-ollama":
                template += f"      - OLLAMA_HOST=${{KOS_OLLAMA_HOST}}\n"
                template += f"      - OLLAMA_ORIGINS=${{KOS_OLLAMA_ORIGINS}}\n"
            elif service_name == "kos-vault":
                template += f"      - VAULT_DEV_ROOT_TOKEN_ID=${{KOS_VAULT_ROOT_TOKEN}}\n"
                template += f"      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:${{KOS_VAULT_INTERNAL_PORT}}\n"
                template += f"      - VAULT_ADDR=http://0.0.0.0:${{KOS_VAULT_INTERNAL_PORT}}\n"
            elif service_name == "kos-backend":
                template += f"      - NODE_ENV=${{KOS_ENVIRONMENT}}\n"
                template += f"      - DEBUG=${{KOS_DEBUG}}\n"
                template += f"      - LOG_LEVEL=${{KOS_LOG_LEVEL}}\n"
                template += f"      - JWT_SECRET=${{KOS_JWT_SECRET}}\n"
                template += f"      - POSTGRES_URL=postgresql://${{KOS_POSTGRES_USER}}:${{KOS_POSTGRES_PASSWORD}}@${{KOS_POSTGRES_HOST}}:${{KOS_POSTGRES_INTERNAL_PORT}}/${{KOS_POSTGRES_DB}}\n"
                template += f"      - REDIS_URL=redis://:${{KOS_REDIS_PASSWORD}}@${{KOS_REDIS_HOST}}:${{KOS_REDIS_INTERNAL_PORT}}/${{KOS_REDIS_DB}}\n"
                template += f"      - NEO4J_URL=bolt://${{KOS_NEO4J_USER}}:${{KOS_NEO4J_PASSWORD}}@${{KOS_NEO4J_HOST}}:${{KOS_NEO4J_INTERNAL_PORT}}\n"
            elif service_name == "kos-frontend":
                template += f"      - NODE_ENV=${{KOS_ENVIRONMENT}}\n"
                template += f"      - REACT_APP_API_URL=http://${{KOS_API_HOST}}:${{KOS_API_EXTERNAL_PORT}}\n"
            
            # Volumes
            if service_name in config["volumes"]:
                volume_name = service_name.replace("kos-", "kos_")
                template += f"    volumes:\n"
                template += f"      - {volume_name}_data:{config['volumes'][service_name]}\n"
            
            # Dependencies
            if "dependencies" in service_config:
                template += f"    depends_on:\n"
                for dep in service_config["dependencies"]:
                    template += f"      - {dep}\n"
            
            # Networks
            template += f"    networks:\n"
            template += f"      - ${{KOS_CONTAINER_NETWORK}}\n"
            
            # Restart policy
            template += f"    restart: unless-stopped\n"
            
            # Profiles
            if category == "core":
                template += f"    profiles:\n"
                template += f"      - core\n"
            elif category == "development":
                template += f"    profiles:\n"
                template += f"      - development\n"
            elif category == "monitoring":
                template += f"    profiles:\n"
                template += f"      - monitoring\n"
            elif category == "storage":
                template += f"    profiles:\n"
                template += f"      - storage\n"
            elif category == "security":
                template += f"    profiles:\n"
                template += f"      - security\n"
            elif category == "managers":
                template += f"    profiles:\n"
                template += f"      - managers\n"
    
    # Networks
    template += f"""
# =============================================================================
# NETWORKS
# =============================================================================
networks:
  ${{KOS_CONTAINER_NETWORK}}:
    driver: bridge
    ipam:
      config:
        - subnet: ${{KOS_NETWORK_SUBNET}}
"""
    
    # Volumes
    template += f"""
# =============================================================================
# VOLUMES
# =============================================================================
volumes:
"""
    
    for service_name in config["volumes"].keys():
        volume_name = service_name.replace("kos-", "kos_")
        template += f"  {volume_name}_data:\n"
    
    return template

def update_docker_compose():
    """Update docker-compose.yml with centralized configuration"""
    config = load_centralized_config()
    
    # Generate new docker-compose.yml
    new_content = generate_docker_compose_template(config)
    
    # Write to docker-compose.yml
    docker_compose_path = Path(__file__).parent.parent / "docker-compose.yml"
    
    # Backup existing file
    if docker_compose_path.exists():
        backup_path = docker_compose_path.with_suffix('.yml.backup')
        docker_compose_path.rename(backup_path)
        print(f"Backed up existing docker-compose.yml to {backup_path}")
    
    # Write new file
    with open(docker_compose_path, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {docker_compose_path}")
    print("All hardcoded ports and IPs have been replaced with environment variables!")

def main():
    """Main function"""
    print("Updating docker-compose.yml with centralized configuration...")
    update_docker_compose()
    print("Docker Compose file updated successfully!")

if __name__ == "__main__":
    main() 