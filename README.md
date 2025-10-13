# 🚀 Personal Code Archive

**A comprehensive collection of code examples, projects, and utilities accumulated over years of software development, learning, and experimentation.**

[![Languages](https://img.shields.io/badge/Languages-TypeScript%20%7C%20Python%20%7C%20Rust%20%7C%20C%2B%2B%20%7C%20Java%20%7C%20Go-blue)]()
[![Focus](https://img.shields.io/badge/Focus-System%20Design%20%7C%20AI%2FML%20%7C%20Full%20Stack-green)]()
[![License](https://img.shields.io/badge/License-Educational%20%2F%20Personal-orange)]()

---

## 📖 About This Repository

This repository is my personal code archive spanning multiple years of development work, containing:
- ✅ Production-ready system design implementations
- ✅ AI/ML projects and experiments  
- ✅ Full-stack web applications
- ✅ Microservices architectures
- ✅ Interview preparation solutions
- ✅ Learning examples across 10+ programming languages
- ✅ Utility scripts and automation tools
- ✅ Algorithm implementations and data structures

**Purpose**: To maintain a portable, well-organized backup of my development work that I can use across different computers, workplaces, and environments.

---

## 🗂️ Repository Structure

```
personal_code/
├── code/                   # Main code repository
│   ├── AI/                # AI/ML projects and experiments
│   ├── system_design/     # System design implementations
│   ├── nestjs/            # NestJS applications
│   ├── python/            # Python projects
│   ├── rust/              # Rust learning & projects
│   ├── CPP/               # C++ examples
│   ├── java/              # Java applications
│   ├── javascript/        # JavaScript/TypeScript projects
│   ├── docker/            # Docker & containerization
│   ├── interviewQs/       # Interview prep & LeetCode
│   └── ...                # And many more!
├── scripts/               # Utility scripts
│   ├── bash/              # Bash automation scripts
│   ├── python/            # Python utilities
│   ├── perl/              # Perl scripts
│   └── util/              # General utilities
└── new_computer/          # New machine setup scripts
    ├── brew_installs.sh   # Homebrew package installations
    ├── firstTimeInstall.sh # First-time setup script
    └── ...
```

---

## 🌟 Featured Projects

### 1. 🏗️ Order Processing System (Production-Grade Microservices)
**Path**: `code/system_design/OrderProcessingSystem/OrderProcessingSystemRepo/`

Enterprise-grade microservices architecture implementing a complete order processing system.

**Tech Stack**: TypeScript, Node.js, Express, PostgreSQL, Redis, AWS SQS, Docker

**Features**:
- JWT/OAuth2 authentication with Passport.js
- Event-driven architecture using AWS SQS
- Redis-based idempotency for reliable message processing
- Circuit breaker pattern (Opossum)
- Retry mechanisms (axios-retry)
- Database connection pooling
- Comprehensive testing (Jest, Mocha, Sinon)
- OpenAPI/Swagger documentation
- Auto-scaling design

**Documentation**: See `SYSTEM_DESIGN.md`, `DESIGN_ANALYSIS.md`, `MANUAL_E2E_TESTING_GUIDE.md`

---

### 2. 🤖 AI/ML Projects

#### LLM Transformer Components (`code/AI/cursor/llm/`)
Educational implementation of transformer architecture from scratch.
- Multi-head attention mechanism
- Positional encoding
- Feed-forward networks
- Layer normalization
- **Tech**: Python, NumPy, PyTorch

#### MCP Server (`code/AI/MCP/toyMCP/`)
Production-ready JSON-RPC server implementing Model Context Protocol.
- RESTful JSON-RPC API
- Passport.js authentication
- PostgreSQL with connection pooling
- Docker containerization
- **Tech**: Node.js, Express, PostgreSQL

#### AI Experiments
- RAG (Retrieval-Augmented Generation) implementations
- CrewAI agent systems
- DeepSeek API integration
- Streamlit applications

---

### 3. 🚢 NestJS Applications (`code/nestjs/`)

#### Task Management System
**Path**: `code/nestjs/zero2heroUdemyCourse/nestjs-course-task-management/`

Enterprise-grade task management API with full authentication.

**Features**:
- JWT authentication & authorization
- TypeORM with PostgreSQL
- CRUD operations with user isolation
- Guards, interceptors, custom pipes
- Configuration management
- Comprehensive testing

---

### 4. 🦀 Rust Learning Projects (`code/rust/`)

Comprehensive Rust examples covering:
- Ownership, borrowing, and lifetimes
- Smart pointers and traits
- Concurrency patterns
- Error handling
- Data structures
- 200+ example programs

---

### 5. 🧵 C++ Concurrency Examples (`code/CPP/concurrency/`)

Thread synchronization patterns:
- Mutex and RAII lock guards
- Semaphores (producer-consumer)
- Condition variables
- Race condition demonstrations

---

### 6. 🎓 Interview Preparation (`code/interviewQs/leetcode/`)

Solutions to coding problems in Python, C++, and JavaScript:
- Arrays, strings, dynamic programming
- Trees, graphs, and algorithms
- Concurrency problems
- System design questions

---

## 🛠️ Technologies & Skills Demonstrated

### Languages (by proficiency)
```
Expert:       TypeScript, JavaScript, Python
Advanced:     Rust, C++, Java, Bash
Intermediate: Go, C, Perl, Ruby
```

### Backend Frameworks
- **Node.js**: NestJS, Express.js
- **Python**: FastAPI, Flask
- **Testing**: Jest, Mocha, Sinon, pytest

### Databases & Caching
- PostgreSQL (with connection pooling)
- Redis (caching, idempotency)
- SQLite
- TypeORM, Sequelize

### Cloud & DevOps
- Docker & Docker Compose
- AWS Services (SQS)
- CI/CD practices
- Infrastructure as Code

### Architecture Patterns
- Microservices
- Event-driven architecture
- Circuit breaker pattern
- Retry mechanisms
- Idempotency patterns
- Repository pattern
- Dependency injection

### AI/ML
- Transformer architectures
- PyTorch, NumPy
- LLM APIs (OpenAI, DeepSeek)
- RAG systems

---

## 📚 Learning Resources Included

This repository contains materials from:
- ✅ Udemy courses (NestJS, Python, Rust, Node.js ML)
- ✅ LeetCode problem solving
- ✅ System design practice
- ✅ Conference materials
- ✅ Design patterns implementations
- ✅ Language-specific best practices

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ (for JavaScript/TypeScript projects)
- **Python** 3.8+ (for Python projects)
- **Rust** 1.70+ (for Rust projects)
- **Docker** & Docker Compose (for containerized projects)
- **PostgreSQL** (for database projects)

### Running Featured Projects

#### Order Processing System
```bash
cd code/system_design/OrderProcessingSystem/OrderProcessingSystemRepo
npm install
cp env.example .env
# Edit .env with your configuration
docker-compose up -d
npm run build
npm run start:order-service &
npm run start:delivery-service &
```

#### MCP Server
```bash
cd code/AI/MCP/toyMCP
npm install
cp .env.example .env
# Configure database credentials
docker-compose up -d
npm test
npm start
```

#### NestJS Task Management
```bash
cd code/nestjs/zero2heroUdemyCourse/nestjs-course-task-management
npm install
# Configure config/development.yml
npm start
```

---

## 🧪 Testing

Most projects include comprehensive test suites:

```bash
# TypeScript/JavaScript projects
npm test                    # Unit tests
npm run test:integration    # Integration tests
npm run test:e2e           # End-to-end tests
npm run test:cov           # With coverage

# Python projects
pytest                      # Run all tests
pytest --cov               # With coverage
pytest -v                  # Verbose output
```

---

## 🔒 Security & Privacy

This repository has been thoroughly sanitized for public/private sharing:

### ✅ Security Validation Completed
- All API keys replaced with placeholders
- No active tokens or secrets
- Database credentials use environment variables
- Internal company URLs removed where appropriate
- Test credentials clearly marked

### ⚠️ Files Requiring Attention

Before using certain projects, you should:

1. **Replace placeholder credentials**:
   - `code/python/ai/deepseek/demo*.py` - Add your DeepSeek API key
   - Various `env.example` files - Configure with your credentials

2. **Review and update**:
   - `code/python/sap/cfPortalLogin/main.py` - Contains test SAP credentials (should be removed if not needed)
   - Any `config/*.yml` files

3. **Generate your own certificates**:
   - PKI examples in various directories
   - Use provided `scripts/bash/pki_generator.sh` for testing

### Best Practices
- Always copy `env.example` to `.env` and configure properly
- Never commit real credentials
- Review configuration files before deployment
- Use secrets management in production

---

## 🔧 Utility Scripts Collection

**Path**: `scripts/`

Useful scripts for automation and system administration:

### Bash Scripts
- **PKI/Certificate Management**: `pki_generator.sh` and variants
- **Security**: `secure-dir.sh` (encrypted APFS disk images)
- **Backup**: `manage_backups.sh`, rsync utilities
- **Development**: `rust_cleaner.sh`, build helpers

### Python Utilities
- GUI examples (Tkinter)
- Network utilities
- Threading examples
- Custom modules

### Setup Scripts
**Path**: `new_computer/`
- `brew_installs.sh` - Install all Homebrew packages
- `firstTimeInstall.sh` - First-time Mac setup
- `clone_git_repos.sh` - Clone repositories

See `scripts/README.md` for detailed documentation.

---

## 📊 Repository Statistics

- **Total Files**: 5600+
- **Languages**: 10+ programming languages
- **TypeScript Files**: 1300+
- **Python Files**: 600+
- **JavaScript Files**: 500+
- **Years Accumulated**: Multiple years of development work

---

## 💡 Use Cases

This repository serves as:

1. **Portfolio**: Demonstrates skills across multiple domains
2. **Learning Resource**: Reference implementations and examples
3. **Code Backup**: Portable archive of personal work
4. **Quick Start Templates**: Boilerplate for new projects
5. **Interview Prep**: Ready-to-review algorithms and patterns
6. **Knowledge Base**: Years of accumulated solutions

---

## 🎯 Key Highlights by Domain

### System Design & Architecture
- ✅ Production-ready microservices
- ✅ Event-driven architectures
- ✅ Scalability patterns
- ✅ Resilience patterns (circuit breakers, retries)

### Security
- ✅ JWT/OAuth2 authentication
- ✅ Certificate generation and PKI
- ✅ Encrypted storage solutions
- ✅ Input validation and sanitization

### Performance
- ✅ Database connection pooling
- ✅ Redis caching strategies
- ✅ Efficient algorithms
- ✅ Concurrency patterns

### Testing
- ✅ Unit, integration, and E2E tests
- ✅ Test coverage reporting
- ✅ Mocking and stubbing patterns
- ✅ BDD/TDD examples

---

## 🔄 Staying Up-to-Date

This repository is continuously updated with:
- New learning projects
- Experimental implementations
- Updated best practices
- Latest technology explorations

---

## 📝 Documentation Standards

Major projects include:
- 📐 Architecture diagrams
- 📖 API documentation (Swagger/OpenAPI)
- 📋 Design documents
- 🧪 Testing guides
- 🚀 Deployment instructions
- 📊 Performance analysis

---

## 🤝 Usage & Contribution

### For Personal Use
- Clone and use as reference
- Fork for your own learning
- Adapt code for your projects

### Questions?
While this is a personal archive, feel free to:
- Open issues for questions
- Suggest improvements
- Share feedback

---

## 📄 License

This repository is for **educational and personal reference purposes**. Individual projects may have different licenses. Third-party code is properly attributed.

---

## 🎓 Skills Demonstrated

This repository demonstrates proficiency in:

### Software Engineering
- Clean code principles
- SOLID design principles
- Design patterns
- Test-driven development
- Documentation best practices

### System Architecture
- Microservices design
- Event-driven systems
- RESTful API design
- Database schema design
- Scalability patterns

### DevOps & Operations
- Containerization (Docker)
- Configuration management
- Logging and monitoring
- Error handling strategies
- Security best practices

---

## 🌐 Connect & Share

This archive represents years of continuous learning and development across multiple technologies. It serves as both a portfolio and a practical backup solution for smooth transitions between development environments.

---

## 🗺️ Future Additions

Planned additions and improvements:
- More AI/ML implementations
- Kubernetes deployment examples
- GraphQL API examples
- More system design patterns
- Performance benchmarking examples

---

**Last Updated**: October 2025

**Repository Purpose**: Personal code archive, learning resource, and portable development backup

**Status**: Actively maintained and continuously updated

---

*This repository reflects a commitment to continuous learning and best practices in software development.*

