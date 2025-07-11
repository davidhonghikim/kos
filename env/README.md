# kOS Environment Configuration

This directory contains all environment configuration files for the kOS system. The files are organized by purpose and loaded in a specific order to provide a clean separation of concerns.

## File Organization

### Core Configuration Files
- **`local.env.example`** - Local services configuration (defaults: true)
- **`cloud.env.example`** - Cloud services configuration (defaults: false)
- **`api-keys.env.example`** - API keys and secrets (blank defaults)
- **`settings.env.example`** - System settings and feature flags

### User Override Files (not in git)
- **`local.env`** - Your local service overrides
- **`cloud.env`** - Your cloud service overrides
- **`api-keys.env`** - Your actual API keys
- **`settings.env`** - Your system settings

## Loading Order

The system loads environment files in this priority order (later files override earlier ones):

1. **`env/local.env.example`** - Base local configuration
2. **`env/cloud.env.example`** - Base cloud configuration
3. **`env/api-keys.env.example`** - Base API keys structure
4. **`env/settings.env.example`** - Base system settings
5. **`env/local.env`** - Your local overrides
6. **`env/cloud.env`** - Your cloud overrides
7. **`env/api-keys.env`** - Your actual API keys
8. **`env/settings.env`** - Your system settings

## Quick Start

1. Copy the example files to create your configuration:
   ```bash
   cp env/local.env.example env/local.env
   cp env/cloud.env.example env/cloud.env
   cp env/api-keys.env.example env/api-keys.env
   cp env/settings.env.example env/settings.env
   ```

2. Edit the files to configure your services:
   - **`local.env`** - Enable/disable local services
   - **`cloud.env`** - Enable/disable cloud services
   - **`api-keys.env`** - Add your API keys
   - **`settings.env`** - Configure system behavior

3. Use the toggle script to manage settings:
   ```bash
   python scripts/toggle_settings.py --help
   ```

## Service Categories

### Local Services (default: true)
- **Core**: PostgreSQL, Redis, Neo4j, Nginx
- **Development**: Gitea, OpenWebUI, Ollama, Supabase
- **Optional**: Elasticsearch, Weaviate, MinIO, Prometheus, Grafana
- **Security**: Vault
- **Managers**: Prompt Manager, Artifact Manager

### Cloud Services (default: false)
- **LLM**: OpenAI, Anthropic, Google AI, Azure OpenAI
- **Storage**: AWS S3, GCP Storage, Azure Storage
- **Vector DBs**: Pinecone, Weaviate Cloud, Qdrant Cloud
- **Databases**: Supabase Cloud, PlanetScale, Neon
- **Monitoring**: Sentry, Datadog, New Relic
- **Auth**: Auth0, Clerk, Supabase Auth
- **Payments**: Stripe, PayPal
- **CDN**: Cloudflare, ImageKit

## Security Notes

- **Never commit** `api-keys.env` to git
- **Never commit** any `.env` files (they're in `.gitignore`)
- Use strong, unique passwords for master credentials
- Generate random secrets for JWT, encryption, and session keys
- Rotate API keys regularly

## Configuration Management

### Command Line
```bash
# Enable a service
python scripts/toggle_settings.py --enable KOS_ENABLE_POSTGRES

# Disable a service
python scripts/toggle_settings.py --disable KOS_ENABLE_ELASTICSEARCH

# List current settings
python scripts/toggle_settings.py --list
```

### Direct File Editing
Edit any `.env` file directly to change settings. The system will reload automatically.

### Environment Variables
Set environment variables to override file settings:
```bash
export KOS_ENABLE_POSTGRES=false
```

### Docker Compose Profiles
Use Docker Compose profiles to control which services start:
```bash
# Start only core services
docker-compose --profile core up

# Start all services
docker-compose --profile all up
```

## Troubleshooting

### Service Not Starting
1. Check if the service is enabled in your `.env` files
2. Verify API keys are set (for cloud services)
3. Check port conflicts
4. Review Docker Compose logs

### Configuration Not Loading
1. Verify file paths are correct
2. Check file permissions
3. Ensure no syntax errors in `.env` files
4. Restart the application

### API Key Issues
1. Verify API keys are correctly set in `api-keys.env`
2. Check if the service is enabled in `cloud.env`
3. Test API key validity
4. Check rate limits and quotas

## Best Practices

1. **Start Local**: Begin with local services only
2. **Add Cloud Gradually**: Enable cloud services one at a time
3. **Test Each Service**: Verify each service works before adding the next
4. **Use Feature Flags**: Leverage the toggle system for easy management
5. **Monitor Resources**: Watch system resources when running many services
6. **Backup Configurations**: Keep backups of your working configurations 