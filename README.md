# kOS - Kind-AI Operating System

[![CI/CD Pipeline](https://github.com/davidhonghikim/kos/actions/workflows/ci.yml/badge.svg)](https://github.com/davidhonghikim/kos/actions/workflows/ci.yml)
[![PR Checks](https://github.com/davidhonghikim/kos/actions/workflows/pr.yml/badge.svg)](https://github.com/davidhonghikim/kos/actions/workflows/pr.yml)
[![Code Coverage](https://codecov.io/gh/davidhonghikim/kos/branch/main/graph/badge.svg)](https://codecov.io/gh/davidhonghikim/kos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org/)

## Overview

kOS (Kind-AI Operating System) is a comprehensive knowledge management and agent orchestration system built on the Knowledge Library Framework (KLF). It provides a unified platform for AI agents to collaborate, share knowledge, and execute complex workflows.

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ 
- **Python** 3.10+
- **Docker** and Docker Compose
- **Git**

### Installation

```bash
# Clone the repository
git clone https://github.com/davidhonghikim/kos.git
cd kos

# Install dependencies
npm install
pip install -r requirements.txt

# Set up environment
cp env/local.env.example env/local.env
cp env/ports.env.example env/ports.env
cp env/api-keys.env.example env/api-keys.env

# Start development environment
docker-compose up -d
npm run dev
```

### Development

```bash
# Run tests
npm test
pytest

# Run linting
npm run lint
npm run format:check

# Build application
npm run build
```

## 🏗️ Architecture

kOS is built with a modular, microservices-based architecture:

- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Python + FastAPI + gRPC
- **Databases**: PostgreSQL, Redis, Neo4j
- **Containerization**: Docker Compose
- **Testing**: Jest, Pytest (90% coverage required)

## 📁 Project Structure

```
kos/
├── src/                    # Source code
│   ├── frontend/          # React/TypeScript frontend
│   ├── backend/           # Python FastAPI backend
│   ├── core/              # Core system components
│   └── shared/            # Shared utilities
├── tests/                 # Test suite
├── docs/                  # JSON documentation for agents
├── config/                # Configuration files
├── env/                   # Environment variables
├── docker/                # Docker configurations
└── agents/                # Agent handoff system
```

## 🎯 Key Features

- **Knowledge Library Framework (KLF)**: Production-ready messaging system
- **Kitchen/Pantry System**: Modular recipe execution architecture
- **Multi-Agent Chat**: Real-time agent collaboration
- **Browser Extension**: Seamless integration with web browsers
- **Service Management**: Comprehensive service orchestration
- **Modular Architecture**: Plug-and-play component system

## 🛠️ Development Standards

- **No Hardcoded Values**: All configuration uses environment variables
- **Modular Code**: Files under 300 lines with single responsibility
- **JSON Documentation**: Agent-focused documentation in JSON format
- **90% Test Coverage**: Comprehensive testing requirements
- **Type Safety**: Full TypeScript and Python type checking

## 📚 Documentation

- **[Contributing Guide](docs/contributing.json)** - Development guidelines
- **[Development Standards](docs/development-standards.json)** - Coding standards
- **[Code Quality Guidelines](docs/code-quality-guidelines.json)** - Quality requirements
- **[Project Analysis](agents/LATEST/)** - Agent handoff documentation

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/contributing.json) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following our standards
4. Run tests and ensure 90% coverage
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/davidhonghikim/kos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/davidhonghikim/kos/discussions)
- **Documentation**: Check the `docs/` directory for detailed guides

## 🏆 Project Status

- **Phase**: Implementation Ready
- **Completion**: 25%
- **Next Milestone**: Core KLF Implementation
- **Timeline**: 20 weeks total

---

**Built with ❤️ by the kOS Development Team**

## Configuration and Environment Management

- All configuration values must come from environment variables or be expanded at runtime.
- The `config/centralized_ports.json` and `config/centralized_config.json` files should use `${ENV_VAR}` references for all sensitive or environment-specific values.
- Use `scripts/generate_env_from_centralized.py` to generate env files from centralized config.
- At runtime, use `scripts/expand-config.js` to expand any config file with environment variables:

```sh
node scripts/expand-config.js config/centralized_config.json > config/expanded_config.json
```

- **No hardcoded values**: All ports, credentials, and service endpoints must be injected via env files or expanded at runtime.

---
