# Python Practice Plan - Senior Developer Edition

**Target Audience**: 30+ years programming experience  
**Time Commitment**: 10-15 minutes daily  
**Focus Areas**: Idioms, Data Structures, Algorithms, Libraries  
**Approach**: Hands-on, progressive mastery

---

## Philosophy

This plan is designed for deep mastery through consistent micro-practice. Each session is standalone but builds upon previous knowledge. The focus is on Python-specific excellence, not basic programming concepts.

---

## 12-Week Rotating Curriculum (Repeats with Increasing Depth)

### **Cycle 1: Weeks 1-12** (Foundation & Idioms)

#### Week 1: Pythonic Idioms
- **Day 1**: List comprehensions vs generator expressions (memory profiling)
- **Day 2**: Dictionary comprehensions and defaultdict patterns
- **Day 3**: Unpacking and tuple swapping idioms
- **Day 4**: Context managers - implementing `__enter__` and `__exit__`
- **Day 5**: EAFP vs LBYL - exception handling patterns
- **Day 6**: Chaining comparisons and walrus operator (`:=`)
- **Day 7**: Review & mini-challenge: Refactor imperative code to Pythonic style

#### Week 2: Iterator Protocol & Generators
- **Day 1**: Implementing custom iterators (`__iter__`, `__next__`)
- **Day 2**: Generator functions and `yield`
- **Day 3**: `itertools` module deep dive (islice, chain, groupby)
- **Day 4**: Generator expressions for pipeline processing
- **Day 5**: `yield from` and generator delegation
- **Day 6**: Infinite generators and `itertools.cycle`
- **Day 7**: Challenge: Build a custom data pipeline with generators

#### Week 3: Advanced Data Structures (collections module)
- **Day 1**: `Counter` - frequency counting and most_common
- **Day 2**: `deque` - efficient queues and rotation operations
- **Day 3**: `defaultdict` - avoiding KeyError gracefully
- **Day 4**: `OrderedDict` vs dict (Python 3.7+)
- **Day 5**: `ChainMap` - layered dictionary lookups
- **Day 6**: `namedtuple` and `typing.NamedTuple`
- **Day 7**: Challenge: Implement LRU cache using OrderedDict/deque

#### Week 4: Functional Programming
- **Day 1**: `map`, `filter`, `reduce` - when to use vs comprehensions
- **Day 2**: `functools.partial` and `functools.wraps`
- **Day 3**: `functools.lru_cache` for memoization
- **Day 4**: Higher-order functions and closures
- **Day 5**: `operator` module for functional composition
- **Day 6**: Pure functions and immutability patterns
- **Day 7**: Challenge: Solve problem using only functional style

#### Week 5: Decorators
- **Day 1**: Basic decorator syntax and function wrapping
- **Day 2**: Decorators with arguments
- **Day 3**: Class decorators and `@staticmethod/@classmethod`
- **Day 4**: `@property` and computed attributes
- **Day 5**: Stacking decorators - order matters
- **Day 6**: `functools.singledispatch` for function overloading
- **Day 7**: Challenge: Build timing/logging decorator with statistics

#### Week 6: Algorithms - Sorting & Searching
- **Day 1**: Custom sort keys with `sorted()` and `list.sort()`
- **Day 2**: Binary search with `bisect` module
- **Day 3**: Implementing quicksort with partitioning
- **Day 4**: Merge sort and divide-and-conquer patterns
- **Day 5**: Topological sort (Kahn's algorithm)
- **Day 6**: Searching with `heapq.nsmallest/nlargest`
- **Day 7**: Challenge: Sort complex objects with multiple criteria

#### Week 7: Algorithms - Graph & Trees
- **Day 1**: Graph representations (adjacency list/matrix)
- **Day 2**: BFS implementation with collections.deque
- **Day 3**: DFS recursive and iterative approaches
- **Day 4**: Dijkstra's algorithm with heapq
- **Day 5**: Binary tree traversals (in/pre/post-order)
- **Day 6**: Trie implementation for prefix matching
- **Day 7**: Challenge: Solve a graph problem (shortest path variant)

#### Week 8: Algorithms - Dynamic Programming
- **Day 1**: Memoization with `@lru_cache`
- **Day 2**: Bottom-up tabulation patterns
- **Day 3**: Knapsack problem (0/1 and unbounded)
- **Day 4**: Longest common subsequence
- **Day 5**: Coin change problem
- **Day 6**: Edit distance (Levenshtein)
- **Day 7**: Challenge: Identify and solve a DP problem

#### Week 9: Standard Library - Text & Data
- **Day 1**: `re` module - advanced regex patterns
- **Day 2**: `string.Template` vs f-strings vs format
- **Day 3**: `json` - custom encoders/decoders
- **Day 4**: `csv` and `DictReader/DictWriter`
- **Day 5**: `pathlib.Path` for file operations
- **Day 6**: `io.StringIO` and `io.BytesIO`
- **Day 7**: Challenge: Parse and transform structured data

#### Week 10: Standard Library - System & OS
- **Day 1**: `argparse` for CLI interfaces
- **Day 2**: `subprocess` - running external commands safely
- **Day 3**: `logging` - handlers, formatters, and levels
- **Day 4**: `datetime` and `zoneinfo` for timezone handling
- **Day 5**: `tempfile` for temporary file management
- **Day 6**: `shutil` for file operations
- **Day 7**: Challenge: Build a CLI tool with proper logging

#### Week 11: Concurrency & Parallelism
- **Day 1**: `threading` basics and GIL implications
- **Day 2**: `multiprocessing` for CPU-bound tasks
- **Day 3**: `concurrent.futures.ThreadPoolExecutor`
- **Day 4**: `concurrent.futures.ProcessPoolExecutor`
- **Day 5**: Thread-safe queues and locks
- **Day 6**: Race conditions and debugging concurrent code
- **Day 7**: Challenge: Parallelize a data processing task

#### Week 12: Async Programming
- **Day 1**: `async`/`await` basics
- **Day 2**: `asyncio.gather` and concurrent coroutines
- **Day 3**: `asyncio.Queue` for async workflows
- **Day 4**: Mixing sync and async code with `run_in_executor`
- **Day 5**: `aiohttp` for async HTTP requests
- **Day 6**: `asyncio.Semaphore` for rate limiting
- **Day 7**: Challenge: Build async web scraper/API client

---

### **Cycle 2: Weeks 13-24** (Advanced Patterns & Libraries)

#### Week 13: Type Hints & Protocols
- **Day 1**: Basic type hints and `mypy`
- **Day 2**: Generic types with `TypeVar`
- **Day 3**: `Protocol` for structural subtyping
- **Day 4**: `Union`, `Optional`, and `Literal` types
- **Day 5**: `Callable` and function type signatures
- **Day 6**: Runtime type checking with `typing.get_type_hints`
- **Day 7**: Challenge: Add complete type hints to existing code

#### Week 14: Metaclasses & Descriptors
- **Day 1**: Understanding `type()` and metaclasses
- **Day 2**: Custom metaclasses for class validation
- **Day 3**: Descriptor protocol (`__get__`, `__set__`, `__delete__`)
- **Day 4**: Property implementation using descriptors
- **Day 5**: Class decorators vs metaclasses
- **Day 6**: `__init_subclass__` hook
- **Day 7**: Challenge: Build a validation framework with descriptors

#### Week 15: Magic Methods (Dunder Methods)
- **Day 1**: `__repr__` vs `__str__` best practices
- **Day 2**: Container methods (`__len__`, `__getitem__`, `__setitem__`)
- **Day 3**: Comparison methods (`__eq__`, `__lt__`, `@total_ordering`)
- **Day 4**: Numeric methods (`__add__`, `__mul__`, etc.)
- **Day 5**: `__call__` for callable objects
- **Day 6**: `__hash__` and hashable types
- **Day 7**: Challenge: Implement a custom collection class

#### Week 16: Context Managers & Resource Management
- **Day 1**: `contextlib.contextmanager` decorator
- **Day 2**: `contextlib.ExitStack` for dynamic contexts
- **Day 3**: `contextlib.suppress` for exception handling
- **Day 4**: Async context managers (`__aenter__`, `__aexit__`)
- **Day 5**: Reusable vs single-use context managers
- **Day 6**: `contextlib.closing` pattern
- **Day 7**: Challenge: Build a transactional resource manager

#### Week 17: Testing & Quality
- **Day 1**: `pytest` fixtures and parameterization
- **Day 2**: `unittest.mock` - patch, MagicMock, side_effect
- **Day 3**: Property-based testing with `hypothesis`
- **Day 4**: Test coverage with `coverage.py`
- **Day 5**: `doctest` for documentation testing
- **Day 6**: `tox` for multi-environment testing
- **Day 7**: Challenge: Achieve 100% coverage on a module

#### Week 18: Data Science - NumPy
- **Day 1**: Array creation and broadcasting rules
- **Day 2**: Indexing, slicing, and boolean masking
- **Day 3**: Universal functions (ufuncs) and vectorization
- **Day 4**: Array operations (reshape, transpose, stack)
- **Day 5**: Linear algebra with `np.linalg`
- **Day 6**: Performance: views vs copies
- **Day 7**: Challenge: Implement algorithm using vectorized ops

#### Week 19: Data Science - Pandas
- **Day 1**: Series and DataFrame fundamentals
- **Day 2**: Selection with `.loc`, `.iloc`, and boolean indexing
- **Day 3**: GroupBy operations and aggregation
- **Day 4**: Merge, join, and concat operations
- **Day 5**: Method chaining and pipe
- **Day 6**: Performance optimization with categories and chunking
- **Day 7**: Challenge: Complex data transformation pipeline

#### Week 20: Web & HTTP
- **Day 1**: `requests` - sessions, auth, and retries
- **Day 2**: `urllib` and `http.client` lower-level access
- **Day 3**: `FastAPI` basics - path operations and validation
- **Day 4**: `pydantic` models for data validation
- **Day 5**: `httpx` for async HTTP
- **Day 6**: Rate limiting and backoff strategies
- **Day 7**: Challenge: Build a REST API client with retry logic

#### Week 21: Database & ORM
- **Day 1**: `sqlite3` and connection management
- **Day 2**: SQL injection prevention and parameterized queries
- **Day 3**: `SQLAlchemy` Core - table definitions
- **Day 4**: `SQLAlchemy` ORM - models and relationships
- **Day 5**: Query optimization and eager loading
- **Day 6**: Database migrations with `alembic`
- **Day 7**: Challenge: Design schema and implement CRUD operations

#### Week 22: Performance Optimization
- **Day 1**: `timeit` and `cProfile` for profiling
- **Day 2**: `memory_profiler` and object size analysis
- **Day 3**: `__slots__` for memory optimization
- **Day 4**: List vs tuple vs set performance characteristics
- **Day 5**: `array.array` and `struct` for compact data
- **Day 6**: C extensions with `ctypes` or `cffi`
- **Day 7**: Challenge: Optimize slow code (10x+ improvement)

#### Week 23: Security & Best Practices
- **Day 1**: Input validation and sanitization
- **Day 2**: `secrets` module for cryptographic randomness
- **Day 3**: `hashlib` and password hashing (bcrypt, argon2)
- **Day 4**: SQL injection and XSS prevention
- **Day 5**: `pickle` security concerns and alternatives
- **Day 6**: Environment variables and `python-dotenv`
- **Day 7**: Challenge: Security audit of existing code

#### Week 24: Design Patterns in Python
- **Day 1**: Singleton (and why to avoid it)
- **Day 2**: Factory and Abstract Factory
- **Day 3**: Builder pattern with fluent interfaces
- **Day 4**: Strategy pattern with functions
- **Day 5**: Observer pattern and event systems
- **Day 6**: Command pattern for undo/redo
- **Day 7**: Challenge: Refactor code to use appropriate pattern

---

### **Cycle 3: Weeks 25-36** (Expert Topics & Specialization)

#### Week 25: Packaging & Distribution
- **Day 1**: `setup.py` vs `pyproject.toml` (PEP 517/518)
- **Day 2**: `setuptools` - entry points and console scripts
- **Day 3**: `poetry` for dependency management
- **Day 4**: Building wheels and source distributions
- **Day 5**: Publishing to PyPI and TestPyPI
- **Day 6**: Versioning strategies (semantic versioning, `bumpversion`)
- **Day 7**: Challenge: Package and publish a reusable library

#### Week 26: Advanced Itertools & More Collections
- **Day 1**: `itertools.product` and `itertools.combinations`
- **Day 2**: `itertools.accumulate` for running totals
- **Day 3**: `itertools.compress` and `itertools.filterfalse`
- **Day 4**: `itertools.tee` for iterator duplication
- **Day 5**: `more-itertools` library - chunked, windowed, partition
- **Day 6**: Custom iterator combinators
- **Day 7**: Challenge: Build complex data transformation using itertools

#### Week 27: Abstract Base Classes (ABCs)
- **Day 1**: `collections.abc` - Sequence, Mapping, Set interfaces
- **Day 2**: Creating custom ABCs with `abc.ABC`
- **Day 3**: `@abc.abstractmethod` and enforcement
- **Day 4**: Virtual subclasses with `register()`
- **Day 5**: `__subclasshook__` for structural typing
- **Day 6**: Mixin classes and multiple inheritance
- **Day 7**: Challenge: Design extensible plugin system with ABCs

#### Week 28: Memory Management & Garbage Collection
- **Day 1**: Reference counting and `sys.getrefcount()`
- **Day 2**: `gc` module - generational garbage collection
- **Day 3**: Weak references with `weakref` module
- **Day 4**: `__del__` finalizer and cleanup patterns
- **Day 5**: Memory leaks - circular references and debugging
- **Day 6**: Object pooling and reuse patterns
- **Day 7**: Challenge: Debug and fix memory leak in provided code

#### Week 29: Scientific Computing - SciPy
- **Day 1**: `scipy.stats` - statistical distributions and tests
- **Day 2**: `scipy.optimize` - minimization and root finding
- **Day 3**: `scipy.interpolate` for data interpolation
- **Day 4**: `scipy.integrate` for numerical integration
- **Day 5**: `scipy.sparse` for sparse matrices
- **Day 6**: `scipy.signal` for signal processing basics
- **Day 7**: Challenge: Solve optimization problem with constraints

#### Week 30: CLI Tools & Terminal UIs
- **Day 1**: `argparse` advanced - subcommands and argument groups
- **Day 2**: `click` - command groups and options
- **Day 3**: `typer` for modern CLI with type hints
- **Day 4**: `rich` - colored output and progress bars
- **Day 5**: `rich.table` and `rich.console` for formatting
- **Day 6**: `prompt_toolkit` for interactive CLIs
- **Day 7**: Challenge: Build feature-rich CLI tool with subcommands

#### Week 31: Data Validation & Serialization
- **Day 1**: `pydantic` BaseModel and field validation
- **Day 2**: `pydantic` validators and custom validation logic
- **Day 3**: `marshmallow` schemas and nested objects
- **Day 4**: `dataclasses` with validation hooks
- **Day 5**: `attrs` library for class definition
- **Day 6**: JSON Schema validation with `jsonschema`
- **Day 7**: Challenge: Build API request/response validator

#### Week 32: Parsing & AST Manipulation
- **Day 1**: `ast` module - parsing Python source code
- **Day 2**: `ast.NodeVisitor` and `ast.NodeTransformer`
- **Day 3**: Static analysis with `ast` (finding patterns)
- **Day 4**: `lark` parser - grammar definition
- **Day 5**: `pyparsing` for custom DSLs
- **Day 6**: Source code generation and code templates
- **Day 7**: Challenge: Build linter or code transformation tool

#### Week 33: Network Programming
- **Day 1**: `socket` module - TCP client/server basics
- **Day 2**: UDP sockets and datagram protocols
- **Day 3**: `asyncio` protocol - async TCP server
- **Day 4**: `asyncio.start_server` and stream handling
- **Day 5**: WebSocket with `websockets` library
- **Day 6**: `selectors` for I/O multiplexing
- **Day 7**: Challenge: Build async chat server/client

#### Week 34: Cryptography & Security
- **Day 1**: `cryptography` - Fernet symmetric encryption
- **Day 2**: Public key cryptography (RSA, ECC)
- **Day 3**: Digital signatures and verification
- **Day 4**: `hmac` for message authentication
- **Day 5**: `ssl` module and TLS/SSL contexts
- **Day 6**: Key derivation functions (PBKDF2, scrypt)
- **Day 7**: Challenge: Implement secure file encryption tool

#### Week 35: Image Processing
- **Day 1**: `Pillow` - opening, resizing, and saving images
- **Day 2**: Image filters and enhancements
- **Day 3**: Drawing on images with `ImageDraw`
- **Day 4**: `opencv-python` basics - reading and displaying
- **Day 5**: Image transformations (rotation, cropping, perspective)
- **Day 6**: Color space conversions and histograms
- **Day 7**: Challenge: Build batch image processor with filters

#### Week 36: Natural Language Processing
- **Day 1**: Text preprocessing - tokenization and normalization
- **Day 2**: `nltk` - stopwords, stemming, and lemmatization
- **Day 3**: `spaCy` - NER and part-of-speech tagging
- **Day 4**: Text similarity and distance metrics
- **Day 5**: Bag of words and TF-IDF with `scikit-learn`
- **Day 6**: Sentiment analysis basics
- **Day 7**: Challenge: Build text classifier or analyzer

---

### **Cycle 4: Weeks 37-48** (Production & Architecture)

#### Week 37: Logging & Observability
- **Day 1**: `logging` - custom handlers and formatters
- **Day 2**: Structured logging with JSON output
- **Day 3**: Log aggregation patterns (rotating files, syslog)
- **Day 4**: `structlog` for structured logging
- **Day 5**: Distributed tracing concepts and correlation IDs
- **Day 6**: Metrics collection with `prometheus_client`
- **Day 7**: Challenge: Implement comprehensive logging strategy

#### Week 38: Configuration Management
- **Day 1**: `configparser` for INI files
- **Day 2**: YAML configuration with `PyYAML`
- **Day 3**: TOML with `tomli`/`tomllib` (Python 3.11+)
- **Day 4**: Environment-based config with `python-dotenv`
- **Day 5**: `dynaconf` for layered configuration
- **Day 6**: Configuration validation and schema enforcement
- **Day 7**: Challenge: Build multi-environment config system

#### Week 39: Caching Strategies
- **Day 1**: `@lru_cache` deep dive and cache_info
- **Day 2**: `@cache` (Python 3.9+) and unbounded caching
- **Day 3**: `cachetools` - TTL and LFU caches
- **Day 4**: Redis caching with `redis-py`
- **Day 5**: Cache invalidation strategies
- **Day 6**: Distributed caching patterns
- **Day 7**: Challenge: Implement multi-level caching system

#### Week 40: Message Queues & Task Processing
- **Day 1**: `queue.Queue` for thread-safe queues
- **Day 2**: `multiprocessing.Queue` for process communication
- **Day 3**: `celery` basics - tasks and workers
- **Day 4**: `celery` - routing and task prioritization
- **Day 5**: `rq` (Redis Queue) for simple task queuing
- **Day 6**: Error handling and retry strategies
- **Day 7**: Challenge: Build distributed task processing system

#### Week 41: API Design & Documentation
- **Day 1**: RESTful API design principles
- **Day 2**: `FastAPI` - dependency injection system
- **Day 3**: `FastAPI` - background tasks and middleware
- **Day 4**: OpenAPI/Swagger documentation generation
- **Day 5**: API versioning strategies
- **Day 6**: Rate limiting and throttling
- **Day 7**: Challenge: Design and document complete REST API

#### Week 42: GraphQL & Alternative APIs
- **Day 1**: GraphQL basics and schema definition
- **Day 2**: `strawberry` or `graphene` for GraphQL servers
- **Day 3**: Resolvers and data loaders
- **Day 4**: gRPC with `grpcio` basics
- **Day 5**: Protocol Buffers definition
- **Day 6**: Comparing REST vs GraphQL vs gRPC
- **Day 7**: Challenge: Implement GraphQL API for existing data

#### Week 43: Database Advanced Topics
- **Day 1**: Connection pooling and management
- **Day 2**: Transaction isolation levels
- **Day 3**: Database indexing strategies
- **Day 4**: Query optimization and EXPLAIN analysis
- **Day 5**: N+1 query problem and solutions
- **Day 6**: Database sharding and partitioning concepts
- **Day 7**: Challenge: Optimize slow database queries

#### Week 44: Event-Driven Architecture
- **Day 1**: Event sourcing concepts
- **Day 2**: Publisher-subscriber pattern implementation
- **Day 3**: Message brokers - RabbitMQ with `pika`
- **Day 4**: Apache Kafka with `kafka-python`
- **Day 5**: Event schemas and versioning
- **Day 6**: CQRS (Command Query Responsibility Segregation)
- **Day 7**: Challenge: Build event-driven microservice

#### Week 45: Microservices Patterns
- **Day 1**: Service discovery and registration
- **Day 2**: Circuit breaker pattern with `pybreaker`
- **Day 3**: API gateway patterns
- **Day 4**: Service mesh concepts
- **Day 5**: Distributed transactions and saga pattern
- **Day 6**: Health checks and readiness probes
- **Day 7**: Challenge: Implement resilient service communication

#### Week 46: Container & Orchestration
- **Day 1**: `docker-py` - container management
- **Day 2**: Building optimal Docker images for Python
- **Day 3**: Multi-stage builds and layer optimization
- **Day 4**: Docker Compose for local development
- **Day 5**: Kubernetes Python client basics
- **Day 6**: Helm charts for Python applications
- **Day 7**: Challenge: Containerize and deploy application

#### Week 47: Monitoring & Debugging Production
- **Day 1**: `pdb` advanced debugging techniques
- **Day 2**: Remote debugging with `debugpy`
- **Day 3**: `py-spy` for profiling production code
- **Day 4**: Memory profiling in production
- **Day 5**: Error tracking with Sentry integration
- **Day 6**: Application Performance Monitoring (APM)
- **Day 7**: Challenge: Debug production issue simulation

#### Week 48: Code Quality & Static Analysis
- **Day 1**: `pylint` configuration and custom checks
- **Day 2**: `flake8` plugins and enforcement
- **Day 3**: `black` and code formatting standards
- **Day 4**: `isort` for import organization
- **Day 5**: `mypy` strict mode and type coverage
- **Day 6**: `bandit` for security linting
- **Day 7**: Challenge: Set up complete CI/CD quality pipeline

---

### **Cycle 5+: Weeks 49+** (Mastery & Specialization)

Continue with domain-specific deep dives:
- **Machine Learning**: `scikit-learn`, model deployment, MLOps
- **Data Engineering**: `Apache Airflow`, `dask`, `polars`
- **Game Development**: `pygame`, `arcade`
- **GUI Development**: `tkinter`, `PyQt`, `Kivy`
- **Embedded Systems**: `MicroPython`, `CircuitPython`
- **Blockchain**: Web3.py, smart contract interaction
- **Quantum Computing**: `qiskit` basics
- **Bioinformatics**: `biopython`, sequence analysis
- **Financial Analysis**: `pandas-ta`, `zipline`
- **DevOps Automation**: `ansible`, `terraform` Python SDKs

---

## Daily Session Structure (10-15 minutes)

1. **Read/Review** (2-3 min): Concept explanation or documentation
2. **Code Exercise** (7-10 min): Hands-on implementation
3. **Reflect** (1-2 min): Note insights, gotchas, or questions

---

## Complexity Levels

- **Level 1** (Cycles 1-2): Implement concept in isolation
- **Level 2** (Cycles 3-4): Combine concepts, mini-projects
- **Level 3** (Cycles 5+): Architectural decisions, performance trade-offs

---

## Resources

- **Documentation**: docs.python.org (official)
- **Style Guide**: PEP 8, PEP 257 (docstrings)
- **Enhancement Proposals**: Read relevant PEPs for deep understanding
- **Books**: "Fluent Python" by Luciano Ramalho, "Effective Python" by Brett Slatkin
- **Practice**: LeetCode (Medium/Hard), Project Euler

---

## Progress Tracking

See `PRACTICE_LOG.md` for daily tracking and notes.

---

## Customization Notes

- Skip topics you already master (but try the challenge)
- Deep-dive on topics relevant to your domain
- Adjust difficulty based on your progress
- Take "review weeks" to revisit challenging topics

---

**Last Updated**: 2025-11-25  
**Current Cycle**: 1  
**Current Week**: 1  
**Current Day**: 1 (In Progress)

