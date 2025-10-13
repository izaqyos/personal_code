# Personal Code Repository

This is my comprehensive collection of code examples, projects, and learning materials spanning multiple programming languages and technologies, accumulated over years of software development and learning.

## 🎯 Overview

This repository contains:
- Production-grade system design implementations
- Microservices architectures with TypeScript/Node.js
- AI/ML projects and experiments
- Full-stack applications
- Interview preparation code
- Language-specific learning examples (Rust, C++, Java, Python, Go, etc.)
- Concurrency and systems programming examples

## 🏗️ Featured Projects

### System Design: Order Processing System
**Location:** `system_design/OrderProcessingSystem/OrderProcessingSystemRepo/`

A production-ready microservices-based order processing system demonstrating enterprise architecture patterns.

**Tech Stack:** TypeScript, Node.js, Express, PostgreSQL, Redis, AWS SQS, Docker

**Features:**
- JWT/OAuth2 authentication
- Event-driven architecture with SQS message queues
- Redis-based idempotency
- Circuit breaker pattern (using Opossum)
- Retry mechanisms (using axios-retry)
- Comprehensive test coverage (Jest, Sinon, Mocha)
- Auto-scaling design
- Database transactions and connection pooling
- Swagger/OpenAPI documentation

**Key Files:**
- System Design: `SYSTEM_DESIGN.md`, `DESIGN_ANALYSIS.md`
- Architecture Diagrams: `diagrams/system-architecture.md`
- Implementation: `src/order-service/`, `src/delivery-service/`
- Testing Guide: `MANUAL_E2E_TESTING_GUIDE.md`

**Performance & Security:**
- Implements idempotency for reliable message processing
- Connection pooling for database efficiency
- Redis caching for high-throughput scenarios
- JWT-based authentication with Passport.js
- Input validation and sanitization
- Proper error handling and logging

---

### AI/ML Projects

#### 1. LLM Transformer Components
**Location:** `AI/cursor/llm/`

Educational implementation of core transformer architecture components from scratch.

**Components:**
- Multi-head attention mechanism
- Positional encoding
- Feed-forward networks
- Layer normalization

**Tech Stack:** Python, NumPy, PyTorch

**Key Files:**
- `attention.py` - Attention mechanism implementation
- `positional_encoding.py` - Sinusoidal position encoding
- `transformer_components.py` - Core transformer blocks
- Unit tests with pytest

#### 2. Pomodoro Timer Application
**Location:** `AI/cursor/pomodoro/`

Full-featured Pomodoro timer with statistics tracking and notifications.

**Features:**
- Customizable work/break intervals
- Session statistics and analytics
- Desktop notifications
- Data persistence
- Modern GUI with tkinter

**Tech Stack:** Python, tkinter, pytest

#### 3. Space Invaders Game
**Location:** `AI/cursor/space_invaders/`

Classic Space Invaders game implementation with modern Python.

**Features:**
- Sprite-based graphics
- Collision detection
- High score system
- Sound effects
- Game state management

**Tech Stack:** Python, Pygame

---

### MCP (Model Context Protocol) Server
**Location:** `AI/MCP/toyMCP/`

A production-ready JSON-RPC server implementing the Model Context Protocol for AI agents.

**Features:**
- RESTful JSON-RPC API
- Passport.js authentication (Local & JWT strategies)
- PostgreSQL database with connection pooling
- Swagger/OpenAPI documentation
- Docker containerization
- Comprehensive test suite (unit, integration, e2e)

**Tech Stack:** Node.js, Express, PostgreSQL, Docker, Jest

**Key Endpoints:**
- `/auth/login` - JWT token generation
- `/rpc` - JSON-RPC endpoint for todo operations
- `/api-docs` - Interactive Swagger UI

---

### NestJS Applications
**Location:** `nestjs/`

#### Task Management System
**Location:** `nestjs/zero2heroUdemyCourse/nestjs-course-task-management/`

Enterprise-grade task management API with authentication.

**Features:**
- JWT authentication
- TypeORM with PostgreSQL
- CRUD operations for tasks
- User-specific task management
- Configuration management
- Unit and E2E tests

**Tech Stack:** NestJS, TypeORM, PostgreSQL, Passport, Jest

**Architecture Highlights:**
- Dependency injection
- Guards and interceptors
- Custom pipes for validation
- Repository pattern
- Config service for environment variables

---

### Rust Learning Projects
**Location:** `rust/`

Comprehensive Rust learning examples covering:

#### Core Concepts
- Ownership and borrowing (`ownership/`)
- Lifetimes (`lifetimes/`)
- Smart pointers (`smart-pointers-box/`)
- Traits and generics (`traits/`, `generics/`)
- Error handling (`error-handling/`)

#### Data Structures
- Vectors, HashMaps, Strings
- Slices and references
- Custom structs and enums

#### Advanced Topics
- Closures and iterators
- Testing patterns
- Regular expressions
- Date/time handling

**Highlight Project:** `learning/learn_to_code_with_rust_udemy/`
- Structured curriculum from basics to advanced
- 200+ example programs
- Hands-on projects (Saladworks, Warehouse)

---

### C++ Concurrency Examples
**Location:** `CPP/concurrency/`

**Mutex Synchronization**
- `mutex/wallet.cpp` - Thread-safe wallet implementation
- `mutex/wallet_no_mutex.cpp` - Demonstrates race conditions

**Semaphores**
- `semaphore/semaphore_demo.cpp` - Producer-consumer pattern
- `semaphoresC11.cpp` - C++11 semaphore implementation

**Key Concepts:**
- Thread synchronization
- RAII lock guards
- Condition variables
- Race condition prevention

---

### Interview Preparation
**Location:** `interviewQs/leetcode/`

Solutions to coding interview problems in multiple languages (Python, C++, JavaScript).

**Topics Covered:**
- Arrays and strings
- Dynamic programming
- Trees and graphs
- Concurrency problems
- System design questions

**Example Problems:**
- N-Queens problem
- Best Time to Buy and Sell Stock
- Merge Intervals
- Rotate Array
- Largest Divisible Subset

---

### Docker & Containerization
**Location:** `docker/`

Docker and containerization examples including:
- Multi-container applications
- Docker Compose configurations
- Microservices deployments
- Database containerization

---

### Additional Language Examples

#### Java (`java/`)
- Snake game with GUI (`snake/`)
- Multithreading examples
- Java 8, 9 features (streams, completable futures, modules)
- Network programming
- Performance testing

#### Python (`python/`)
- AI/ML experiments (RAG, CrewAI agents)
- PDF manipulation
- Web scraping
- Udemy course projects (100 days of code)
- Data structures and algorithms

#### Go (`go/`)
- Go basics and idioms
- Concurrency patterns
- Web servers

#### JavaScript/TypeScript (`javascript/`, `typescript/`, `nodejs/`)
- Express.js applications
- Async programming patterns
- Authentication examples
- WebSocket servers
- C++ addons for Node.js

---

## 🛠️ Technologies & Tools

### Languages
Python • TypeScript • JavaScript • Rust • C++ • Java • Go • C • Bash • Perl

### Frameworks & Libraries
- **Backend:** NestJS, Express.js, FastAPI
- **Frontend:** React, Streamlit
- **Testing:** Jest, Mocha, Sinon, pytest
- **ORM:** TypeORM, Sequelize
- **Auth:** Passport.js, JWT, OAuth2

### Databases & Caching
PostgreSQL • Redis • SQLite

### DevOps & Tools
Docker • Docker Compose • Git • AWS (SQS) • CI/CD

### AI/ML
PyTorch • NumPy • OpenAI API • DeepSeek API

---

## 📚 Learning Resources

This repository includes study materials and notes from:
- Udemy courses (NestJS, Python, Rust)
- LeetCode problem solving
- Cracking the Coding Interview
- Design Patterns implementations
- Conference materials
- System design practice

---

## 🚀 Getting Started

### Prerequisites
- Node.js 16+ (for TypeScript/JavaScript projects)
- Python 3.8+ (for Python projects)
- Rust 1.70+ (for Rust projects)
- Docker & Docker Compose (for containerized projects)
- PostgreSQL (for database projects)

### Running Projects

#### Order Processing System
```bash
cd system_design/OrderProcessingSystem/OrderProcessingSystemRepo
npm install
cp env.example .env  # Configure your environment
docker-compose up -d  # Start PostgreSQL, Redis, SQS
npm run build
npm run start:order-service &
npm run start:delivery-service &
```

#### MCP Server
```bash
cd AI/MCP/toyMCP
npm install
cp .env.example .env  # Set DB credentials
docker-compose up -d  # Start PostgreSQL
npm test  # Run tests
npm start  # Start server
```

#### NestJS Task Management
```bash
cd nestjs/zero2heroUdemyCourse/nestjs-course-task-management
npm install
# Configure config/development.yml
npm start
```

---

## 🧪 Testing

Projects include comprehensive test suites:

```bash
# TypeScript projects
npm test                    # Unit tests
npm run test:integration   # Integration tests
npm run test:e2e          # End-to-end tests

# Python projects
pytest                     # Run all tests
pytest --cov              # With coverage
```

---

## 📖 Documentation

Major projects include:
- Architecture diagrams
- API documentation (Swagger/OpenAPI)
- Design documents
- Testing guides
- Deployment instructions

---

## 🔒 Security Notes

This repository has been cleaned and sanitized for public sharing:
- ✅ All API keys and secrets replaced with placeholders
- ✅ Certificates and private keys removed
- ✅ Database credentials removed
- ✅ Configuration files use environment variables

**Before running any project:**
1. Copy `.env.example` to `.env`
2. Set your own credentials and API keys
3. Generate new certificates for SSL/TLS examples

---

## 🤝 Contributing

This is a personal learning repository, but feel free to:
- Open issues for questions
- Suggest improvements
- Fork and experiment

---

## 📄 License

This repository is for educational purposes. Individual projects may have different licenses.

---

## 📬 Contact

For questions or discussions about the code, feel free to open an issue.

---

## ⭐ Highlights by Language

### TypeScript/JavaScript
- 🏆 Production-ready microservices architecture
- 🔐 Authentication systems (JWT, OAuth2)
- 📊 Event-driven architectures
- 🧪 Comprehensive testing patterns

### Python
- 🤖 LLM transformer implementation
- 🎮 Game development (Space Invaders)
- 📊 Data analysis and visualization
- 🔬 AI/ML experiments

### Rust
- 🦀 Ownership and memory safety
- ⚡ Systems programming
- 🔄 Concurrency patterns
- 📚 Comprehensive learning path

### C++
- 🧵 Concurrency and threading
- 🔒 Mutex and semaphore patterns
- ⚡ Performance-critical code
- 🏗️ Data structures

### Java
- 🎮 GUI applications
- 🧵 Multithreading examples
- ☕ Modern Java features (8, 9+)
- 🌐 Network programming

---

*Last updated: October 2025*

