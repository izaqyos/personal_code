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
- ✅ Comprehensive networking study materials (CCNA/CCNP)
- ✅ Obsidian PKM (Personal Knowledge Management) guides
- ✅ Structured Python practice curriculum

**Purpose**: To maintain a portable, well-organized backup of my development work that I can use across different computers, workplaces, and environments.

---

## 🗂️ Repository Structure

```
personal_code/
├── code/                       # Main code repository
│   ├── AI/                    # AI/ML projects and experiments
│   │   ├── articles/          # AI research articles & analysis
│   │   ├── cursor/            # Cursor IDE tools & tracking
│   │   ├── MCP/               # Model Context Protocol implementations
│   │   └── streamlit/         # Streamlit AI applications
│   ├── system_design/         # System design implementations
│   ├── practice/              # Structured learning practice
│   │   ├── python/            # 48-week Python curriculum
│   │   └── ai/                # Prompt engineering practice
│   ├── networking/            # Comprehensive networking guides
│   │   ├── CCNA/              # CCNA study materials & exercises
│   │   ├── CCNP/              # CCNP advanced materials
│   │   ├── Firewalls/         # iptables, nftables, ufw, pf
│   │   ├── VPN/               # IPsec, OpenVPN, WireGuard
│   │   ├── SSL-TLS-PKI/       # Certificates & encryption
│   │   └── ...                # Cellular, Layer1-2, IP-Protocols
│   ├── python/                # Python projects & tools
│   │   └── tools/             # Utility tools (repo_cleaner, etc.)
│   ├── fun/                   # Fun projects & experiments
│   │   └── quiz-app/          # React quiz application
│   ├── nestjs/                # NestJS applications
│   ├── rust/                  # Rust learning & projects
│   ├── CPP/                   # C++ examples
│   ├── java/                  # Java applications
│   ├── javascript/            # JavaScript/TypeScript projects
│   ├── docker/                # Docker & containerization
│   ├── bash/                  # Bash scripts & automation
│   └── interviewQs/           # Interview prep & LeetCode
├── guides/                     # Learning guides & documentation
│   └── obsidian/              # Complete Obsidian PKM course
│       ├── 01-foundations/    # Getting started
│       ├── 02-intermediate/   # Building your system
│       ├── 03-advanced/       # Power user techniques
│       └── 03-plugins/        # Community plugins guide
├── scripts/                    # Utility scripts
│   ├── bash/                  # Bash automation scripts
│   ├── python/                # Python utilities
│   └── util/                  # General utilities
├── new_computer/              # New machine setup scripts
├── LEARNING_ROADMAP.md        # Central learning tracker
└── README.md                  # This file
```

---

## 🎯 Learning Roadmap

> **Central learning hub**: See [`LEARNING_ROADMAP.md`](./LEARNING_ROADMAP.md) for the complete learning tracker.

| Priority | Topic | Status | Path |
|:--------:|-------|--------|------|
| 1 | Python Practice | 🟡 Week 1, Day 2 | `code/practice/python/` |
| 2 | LeetCode Interview Prep | ⚪ Not Started | `code/interviewQs/` |
| 3 | Obsidian PKM | 🟢 Comfortable | `guides/obsidian/` |
| 4 | Networking (CCNA/CCNP) | ⚪ Future | `code/networking/` |
| 5 | Prompt Engineering | 🟡 Started | `code/practice/ai/prompts/` |
| 6 | Rust | 🟡 Midway | `code/rust/` |

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

#### AI Research Articles (`code/AI/articles/`) *(New!)*
In-depth analysis and explanations of cutting-edge AI research:
- **VL-JEPA** (Vision-Language Joint Embedding Predictive Architecture) - comprehensive analysis including architecture explanation, infographics, and LLM comparison
- **AI Thinking Paradigms** - analysis of different AI reasoning approaches

#### Cursor Usage Tracker (`code/AI/cursor/tracking/`) *(New!)*
Python tool for monitoring Cursor IDE usage and generating statistics.
- Usage monitoring and reporting
- Statistics tracking (JSON output)
- **Tech**: Python

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

### 3. 🐍 Python Practice Curriculum (`code/practice/python/`) *(New!)*

A comprehensive **48-week structured Python curriculum** covering:

**Weeks 1-12 (Foundation & Idioms)**:
- Pythonic idioms (list comprehensions, generators, context managers)
- Iterator protocol and generator patterns
- Advanced data structures (Counter, deque, defaultdict, namedtuple)
- Functional programming (map, filter, reduce, lambda, partial)
- Decorators (parameterized, class-based, functools)
- Algorithms (sorting, searching, graph, trees, dynamic programming)

**Current Progress**: Week 1, Day 2 (Dict comprehensions & defaultdict)

**Key Files**:
- `PYTHON_PRACTICE_PLAN.md` - Complete curriculum overview
- `PROJECT_TODO.md` - Progress tracking
- `python_concepts_deep_dives/` - In-depth concept explanations
- `exercises/` - Daily practice files

---

### 4. 🌐 Networking Study Materials (`code/networking/`) *(New!)*

Comprehensive networking study materials for certification preparation and reference:

#### CCNA Materials (`code/networking/CCNA/`)
Complete CCNA 200-301 study guide:
- **6 Core Modules**: Network Fundamentals, Network Access, IP Connectivity, IP Services, Security, Automation
- **Exercises**: CLI drills, Packet Tracer labs, Troubleshooting scenarios
- **Cheatsheets**: Quick reference guides
- **Practice Exams**: Self-assessment tests

#### CCNP Materials (`code/networking/CCNP/`)
Advanced CCNP Enterprise study materials:
- Architecture, Virtualization, Infrastructure
- Network Assurance, Security, Automation

#### Reference Guides
| Topic | Description |
|-------|-------------|
| `Firewalls/` | iptables, nftables, ufw, firewalld, pf |
| `VPN/` | IPsec, OpenVPN, WireGuard, SSL VPN |
| `SSL-TLS-PKI/` | Certificates, TLS, OpenSSL, Let's Encrypt |
| `IP-Protocols/` | TCP, UDP, ICMP, IPv4, IPv6 |
| `NetworkTools/` | Wireshark, tcpdump, nmap, dig |
| `NetworkAccess/` | 802.1x, RADIUS, TACACS+, EAP |
| `Cellular/` | GSM, GPRS, 3G, LTE, 5G |
| `Layer1-2/` | Ethernet, Fiber, MPLS, SONET/SDH |

---

### 5. 📚 Obsidian PKM Guides (`guides/obsidian/`) *(New!)*

Complete course for building a Personal Knowledge Management system with Obsidian:

| Phase | Topic | Content |
|-------|-------|---------|
| **01-Foundations** | Getting Started | Obsidian 101 - core concepts, vault setup |
| **02-Intermediate** | Building Your System | Linking strategies, templates, daily notes, YAML, search, canvas, Zettelkasten/PARA |
| **03-Advanced** | Power User | Dataview queries, Templater automation, CSS snippets, Git integration, Vim navigation, multi-vault strategies, publishing |
| **03-Plugins** | Ecosystem | Top 20 community plugins guide |

**Files Created**: 15+ comprehensive guides with practical examples

---

### 6. 🛠️ Repo Cleaner Tool (`code/python/tools/repo_cleaner/`) *(New!)*

A professional Python package for cleaning build artifacts across multiple programming languages:

**Features**:
- Detects and cleans: Python, Node.js, Java, C/C++, JavaScript frameworks
- Monorepo support
- Safe dry-run mode
- History tracking and undo capability
- Configurable via YAML

**Tech**: Python 3.11+, Click CLI, pytest

**Documentation**: README, QUICKSTART, INSTALL, ARCHITECTURE, USER_GUIDE

---

### 7. 🎮 Quiz Application (`code/fun/quiz-app/`) *(New!)*

A multiplayer quiz application built with React and Vite:

**Features**:
- Real-time multiplayer sync via localStorage
- Multiple quiz topics
- Timer-based questions
- Score tracking and leaderboards
- Responsive design

**Tech Stack**: React, Vite, Playwright (E2E), Vitest (unit tests)

**Deployment**: Vercel-ready with `vercel.json`

**Documentation**: README, TESTING, ARCHITECTURE, DEEP_DIVE

---

### 8. 🚀 Bash Launcher (`code/bash/launcher.sh`) *(New!)*

Comprehensive bash automation script for common development tasks.

---

### 9. 🚢 NestJS Applications (`code/nestjs/`)

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

### 10. 🦀 Rust Learning Projects (`code/rust/`)

Comprehensive Rust examples covering:
- Ownership, borrowing, and lifetimes
- Smart pointers and traits
- Concurrency patterns
- Error handling
- Data structures
- 200+ example programs

---

### 11. 🧵 C++ Concurrency Examples (`code/CPP/concurrency/`)

Thread synchronization patterns:
- Mutex and RAII lock guards
- Semaphores (producer-consumer)
- Condition variables
- Race condition demonstrations

---

### 12. 🎓 Interview Preparation (`code/interviewQs/leetcode/`)

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
- **Python**: FastAPI, Flask, Streamlit
- **Testing**: Jest, Mocha, Sinon, pytest, Playwright, Vitest

### Databases & Caching
- PostgreSQL (with connection pooling)
- Redis (caching, idempotency)
- SQLite
- TypeORM, Sequelize

### Cloud & DevOps
- Docker & Docker Compose
- AWS Services (SQS)
- Vercel deployment
- CI/CD practices (GitHub Actions)
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
- LLM APIs (OpenAI, DeepSeek, Claude)
- RAG systems
- Prompt engineering

### Networking
- CCNA/CCNP level knowledge
- VPN technologies (IPsec, WireGuard, OpenVPN)
- Firewalls (iptables, nftables)
- SSL/TLS and PKI
- Network troubleshooting

---

## 📚 Learning Resources Included

This repository contains materials from:
- ✅ Udemy courses (NestJS, Python, Rust, Node.js ML)
- ✅ LeetCode problem solving
- ✅ System design practice
- ✅ Conference materials
- ✅ Design patterns implementations
- ✅ Language-specific best practices
- ✅ Comprehensive networking certification prep (CCNA/CCNP)
- ✅ Personal knowledge management (Obsidian)

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

#### Quiz App
```bash
cd code/fun/quiz-app
npm install
npm run dev        # Development server
npm test           # Run tests
npm run build      # Production build
```

#### Repo Cleaner Tool
```bash
cd code/python/tools/repo_cleaner
pip install -e .
repo-cleaner --help
repo-cleaner scan /path/to/project
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

# React projects (Vite)
npm run test               # Vitest unit tests
npm run test:e2e           # Playwright E2E
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
- **Automation**: `launcher.sh` (new!)

### Python Utilities
- GUI examples (Tkinter)
- Network utilities
- Threading examples
- Custom modules
- Repo cleaner tool (new!)

### Setup Scripts
**Path**: `new_computer/`
- `brew_installs.sh` - Install all Homebrew packages
- `firstTimeInstall.sh` - First-time Mac setup
- `clone_git_repos.sh` - Clone repositories

See `scripts/README.md` for detailed documentation.

---

## 📊 Repository Statistics

- **Total Files**: 6000+
- **Languages**: 10+ programming languages
- **TypeScript Files**: 1300+
- **Python Files**: 700+
- **JavaScript Files**: 500+
- **Markdown Guides**: 100+
- **Years Accumulated**: Multiple years of development work

### Recent Additions (Past 30 Days)
- 118 files added/modified
- ~19,000 lines of new code and documentation
- 4 major features: Networking guides, Obsidian PKM, Python practice, New tools

---

## 💡 Use Cases

This repository serves as:

1. **Portfolio**: Demonstrates skills across multiple domains
2. **Learning Resource**: Reference implementations and examples
3. **Code Backup**: Portable archive of personal work
4. **Quick Start Templates**: Boilerplate for new projects
5. **Interview Prep**: Ready-to-review algorithms and patterns
6. **Knowledge Base**: Years of accumulated solutions
7. **Certification Prep**: Networking study materials (CCNA/CCNP)
8. **PKM Reference**: Complete Obsidian guide system

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

### Networking
- ✅ CCNA/CCNP certification materials
- ✅ VPN and security guides
- ✅ Protocol deep-dives
- ✅ Troubleshooting guides

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

**Last Updated**: January 2026

**Repository Purpose**: Personal code archive, learning resource, and portable development backup

**Status**: Actively maintained and continuously updated

---

*This repository reflects a commitment to continuous learning and best practices in software development.*
