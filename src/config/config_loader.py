"""
kOS Configuration Loader
Centralized configuration management for all environment variables
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class DatabaseConfig:
    """Database configuration settings"""
    enabled: bool
    host: str
    port: int
    database: str
    username: str
    password: str
    url: str


@dataclass
class SecurityConfig:
    """Security configuration settings"""
    jwt_secret: str
    jwt_algorithm: str
    jwt_expiration: int
    jwt_refresh_expiration: int
    bcrypt_rounds: int


@dataclass
class ServerConfig:
    """Server configuration settings"""
    host: str
    port: int
    api_port: int
    frontend_host: str
    frontend_port: int
    cors_origins: list[str]


class ConfigLoader:
    """Centralized configuration loader for kOS system"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/centralized_config.json"
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file and environment variables"""
        # Load .env file from root directory
        env_file = Path(".env")
        if env_file.exists():
            load_dotenv(env_file)
        else:
            raise FileNotFoundError("No .env file found in project root. Please copy .env.example to .env and configure.")
        
        # Load user.env file for user-specific overrides
        user_env_file = Path("user.env")
        if user_env_file.exists():
            load_dotenv(user_env_file, override=True)
        
        # Load centralized config
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                self._config = json.load(f)
        
        # Override with environment variables
        self._override_from_env()
        
        # Validate required variables
        self._validate_required_vars()
    
    def _override_from_env(self) -> None:
        """Override config values with environment variables"""
        env_mappings = {
            # Core settings
            'KOS_PROJECT_NAME': 'app.name',
            'KOS_ENVIRONMENT': 'app.environment',
            'KOS_DEBUG': 'app.debug',
            'KOS_LOG_LEVEL': 'app.log_level',
            
            # Docker Images
            'KOS_ENABLE_POSTGRES': 'docker_images.postgres.enabled',
            'KOS_POSTGRES_IMAGE': 'docker_images.postgres.image',
            'KOS_POSTGRES_VERSION': 'docker_images.postgres.version',
            
            'KOS_ENABLE_REDIS': 'docker_images.redis.enabled',
            'KOS_REDIS_IMAGE': 'docker_images.redis.image',
            'KOS_REDIS_VERSION': 'docker_images.redis.version',
            
            'KOS_ENABLE_NEO4J': 'docker_images.neo4j.enabled',
            'KOS_NEO4J_IMAGE': 'docker_images.neo4j.image',
            'KOS_NEO4J_VERSION': 'docker_images.neo4j.version',
            
            'KOS_ENABLE_ELASTICSEARCH': 'docker_images.elasticsearch.enabled',
            'KOS_ELASTICSEARCH_IMAGE': 'docker_images.elasticsearch.image',
            'KOS_ELASTICSEARCH_VERSION': 'docker_images.elasticsearch.version',
            
            'KOS_ENABLE_WEAVIATE': 'docker_images.weaviate.enabled',
            'KOS_WEAVIATE_IMAGE': 'docker_images.weaviate.image',
            'KOS_WEAVIATE_VERSION': 'docker_images.weaviate.version',
            
            'KOS_ENABLE_MINIO': 'docker_images.minio.enabled',
            'KOS_MINIO_IMAGE': 'docker_images.minio.image',
            'KOS_MINIO_VERSION': 'docker_images.minio.version',
            
            'KOS_ENABLE_PROMETHEUS': 'docker_images.prometheus.enabled',
            'KOS_PROMETHEUS_IMAGE': 'docker_images.prometheus.image',
            'KOS_PROMETHEUS_VERSION': 'docker_images.prometheus.version',
            
            'KOS_ENABLE_GRAFANA': 'docker_images.grafana.enabled',
            'KOS_GRAFANA_IMAGE': 'docker_images.grafana.image',
            'KOS_GRAFANA_VERSION': 'docker_images.grafana.version',
            
            # Server settings
            'KOS_API_HOST': 'server.host',
            'KOS_API_PORT': 'server.port',
            'KOS_API_CONTAINER_PORT': 'server.container_port',
            'KOS_FRONTEND_HOST': 'server.frontend_host',
            'KOS_FRONTEND_PORT': 'server.frontend_port',
            'KOS_FRONTEND_CONTAINER_PORT': 'server.frontend_container_port',
            'KOS_CORS_ORIGINS': 'server.cors_origins',
            
            # Database settings
            'KOS_ENABLE_POSTGRES': 'databases.postgres.enabled',
            'KOS_POSTGRES_HOST': 'databases.postgres.host',
            'KOS_POSTGRES_PORT': 'databases.postgres.port',
            'KOS_POSTGRES_DB': 'databases.postgres.database',
            'KOS_POSTGRES_USER': 'databases.postgres.username',
            'KOS_POSTGRES_PASSWORD': 'databases.postgres.password',
            'KOS_POSTGRES_URL': 'databases.postgres.url',
            
            'KOS_ENABLE_REDIS': 'databases.redis.enabled',
            'KOS_REDIS_HOST': 'databases.redis.host',
            'KOS_REDIS_PORT': 'databases.redis.port',
            'KOS_REDIS_PASSWORD': 'databases.redis.password',
            'KOS_REDIS_DB': 'databases.redis.database',
            'KOS_REDIS_URL': 'databases.redis.url',
            
            'KOS_ENABLE_NEO4J': 'databases.neo4j.enabled',
            'KOS_NEO4J_HOST': 'databases.neo4j.host',
            'KOS_NEO4J_PORT': 'databases.neo4j.port',
            'KOS_NEO4J_USER': 'databases.neo4j.username',
            'KOS_NEO4J_PASSWORD': 'databases.neo4j.password',
            'KOS_NEO4J_URL': 'databases.neo4j.url',
            
            # Search settings
            'KOS_ENABLE_ELASTICSEARCH': 'search.elasticsearch.enabled',
            'KOS_ELASTICSEARCH_HOST': 'search.elasticsearch.host',
            'KOS_ELASTICSEARCH_PORT': 'search.elasticsearch.port',
            'KOS_ELASTICSEARCH_URL': 'search.elasticsearch.url',
            
            # Vector settings
            'KOS_ENABLE_WEAVIATE': 'vector.weaviate.enabled',
            'KOS_WEAVIATE_HOST': 'vector.weaviate.host',
            'KOS_WEAVIATE_PORT': 'vector.weaviate.port',
            'KOS_WEAVIATE_URL': 'vector.weaviate.url',
            
            # Storage settings
            'KOS_ENABLE_MINIO': 'storage.minio.enabled',
            'KOS_MINIO_HOST': 'storage.minio.host',
            'KOS_MINIO_PORT': 'storage.minio.port',
            'KOS_MINIO_CONSOLE_PORT': 'storage.minio.console_port',
            'KOS_MINIO_ROOT_USER': 'storage.minio.root_user',
            'KOS_MINIO_ROOT_PASSWORD': 'storage.minio.root_password',
            'KOS_MINIO_URL': 'storage.minio.url',
            
            'KOS_STORAGE_TYPE': 'storage.file.type',
            'KOS_STORAGE_PATH': 'storage.file.path',
            'KOS_MAX_FILE_SIZE': 'storage.file.max_file_size',
            'KOS_ALLOWED_FILE_TYPES': 'storage.file.allowed_types',
            
            # Monitoring settings
            'KOS_ENABLE_PROMETHEUS': 'monitoring.prometheus.enabled',
            'KOS_PROMETHEUS_PORT': 'monitoring.prometheus.port',
            'KOS_ENABLE_GRAFANA': 'monitoring.grafana.enabled',
            'KOS_GRAFANA_PORT': 'monitoring.grafana.port',
            'KOS_GRAFANA_ADMIN_PASSWORD': 'monitoring.grafana.admin_password',
            
            # Security settings
            'KOS_JWT_SECRET': 'security.jwt_secret',
            'KOS_JWT_ALGORITHM': 'security.jwt_algorithm',
            'KOS_JWT_EXPIRATION': 'security.jwt_expiration',
            'KOS_JWT_REFRESH_EXPIRATION': 'security.jwt_refresh_expiration',
            'KOS_BCRYPT_ROUNDS': 'security.bcrypt_rounds',
            
            # External services
            'KOS_OPENAI_API_KEY': 'external_services.openai.api_key',
            'KOS_ANTHROPIC_API_KEY': 'external_services.anthropic.api_key',
            'KOS_GOOGLE_API_KEY': 'external_services.google.api_key',
            
            # WebSocket settings
            'KOS_WS_PORT': 'websocket.port',
            'KOS_WS_PATH': 'websocket.path',
            'KOS_WS_HEARTBEAT_INTERVAL': 'websocket.heartbeat_interval',
            
            # Plugin settings
            'KOS_PLUGIN_DIRECTORY': 'plugins.directory',
            'KOS_PLUGIN_REGISTRY_URL': 'plugins.registry_url',
            'KOS_PLUGIN_SANDBOX': 'plugins.sandbox',
            
            # Backup settings
            'KOS_BACKUP_ENABLED': 'backup.enabled',
            'KOS_BACKUP_SCHEDULE': 'backup.schedule',
            'KOS_BACKUP_RETENTION_DAYS': 'backup.retention_days',
            'KOS_BACKUP_PATH': 'backup.path',
            
            # Email settings
            'KOS_SMTP_HOST': 'email.smtp_host',
            'KOS_SMTP_PORT': 'email.smtp_port',
            'KOS_SMTP_USER': 'email.smtp_user',
            'KOS_SMTP_PASSWORD': 'email.smtp_password',
            'KOS_EMAIL_FROM': 'email.from'
        }
        
        for env_var, config_path in env_mappings.items():
            env_value = os.getenv(env_var)
            if env_value is not None:
                self._set_nested_value(config_path, env_value)
    
    def _set_nested_value(self, path: str, value: Any) -> None:
        """Set a nested value in the config dictionary"""
        keys = path.split('.')
        current = self._config
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Convert value based on expected type
        if isinstance(current.get(keys[-1]), int):
            try:
                value = int(value)
            except ValueError:
                pass
        elif isinstance(current.get(keys[-1]), bool):
            value = value.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(current.get(keys[-1]), list):
            value = value.split(',') if isinstance(value, str) else value
        
        current[keys[-1]] = value
    
    def _validate_required_vars(self) -> None:
        """Validate that all required environment variables are set"""
        required_vars = self._config.get('validation_rules', {}).get('required_variables', [])
        missing_vars = []
        
        for var in required_vars:
            if not self.get(var.lower().replace('_', '.')):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}. Please check your .env file.")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by dot notation"""
        keys = key.split('.')
        current = self._config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        
        return current
    
    def get_database_config(self, db_type: str = 'postgres') -> DatabaseConfig:
        """Get database configuration"""
        db_config = self._config.get('databases', {}).get(db_type, {})
        return DatabaseConfig(
            enabled=db_config.get('enabled', False),
            host=db_config.get('host'),
            port=db_config.get('port'),
            database=db_config.get('database'),
            username=db_config.get('username'),
            password=db_config.get('password'),
            url=db_config.get('url')
        )
    
    def get_security_config(self) -> SecurityConfig:
        """Get security configuration"""
        security = self._config.get('security', {})
        return SecurityConfig(
            jwt_secret=security.get('jwt_secret'),
            jwt_algorithm=security.get('jwt_algorithm'),
            jwt_expiration=security.get('jwt_expiration'),
            jwt_refresh_expiration=security.get('jwt_refresh_expiration'),
            bcrypt_rounds=security.get('bcrypt_rounds')
        )
    
    def get_server_config(self) -> ServerConfig:
        """Get server configuration"""
        server = self._config.get('server', {})
        return ServerConfig(
            host=server.get('host'),
            port=server.get('port'),
            api_port=server.get('api_port'),
            frontend_host=server.get('frontend_host'),
            frontend_port=server.get('frontend_port'),
            cors_origins=server.get('cors_origins', [])
        )
    
    def is_service_enabled(self, service_name: str) -> bool:
        """Check if a service is enabled via feature flag"""
        service_configs = {
            'postgres': 'databases.postgres.enabled',
            'redis': 'databases.redis.enabled',
            'neo4j': 'databases.neo4j.enabled',
            'elasticsearch': 'search.elasticsearch.enabled',
            'weaviate': 'vector.weaviate.enabled',
            'minio': 'storage.minio.enabled',
            'prometheus': 'monitoring.prometheus.enabled',
            'grafana': 'monitoring.grafana.enabled'
        }
        
        config_path = service_configs.get(service_name)
        if config_path:
            return self.get(config_path, False)
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Return the complete configuration as a dictionary"""
        return self._config.copy()


# Global configuration instance
config = ConfigLoader() 