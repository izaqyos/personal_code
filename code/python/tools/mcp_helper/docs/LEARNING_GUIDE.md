# Python Learning Guide: MCP Health Check Tool

A curated guide to the noteworthy Python patterns, idioms, and syntax used in this project. Use this as a reference to internalize modern Python best practices.

---

## Table of Contents

1. [Type Hints & Modern Typing](#1-type-hints--modern-typing)
2. [Dataclasses & Pydantic Models](#2-dataclasses--pydantic-models)
3. [Abstract Base Classes & Protocols](#3-abstract-base-classes--protocols)
4. [Enum Patterns](#4-enum-patterns)
5. [Async/Await Patterns](#5-asyncawait-patterns)
6. [Context Managers](#6-context-managers)
7. [Exception Handling](#7-exception-handling)
8. [Path Operations with pathlib](#8-path-operations-with-pathlib)
9. [Testing Patterns](#9-testing-patterns)
10. [CLI with Click](#10-cli-with-click)
11. [Rich Console Output](#11-rich-console-output)
12. [Walrus Operator & Modern Syntax](#12-walrus-operator--modern-syntax)

---

## 1. Type Hints & Modern Typing

### Future Annotations (PEP 563)

```python
from __future__ import annotations  # Always at top of file

# Allows forward references and cleaner syntax
def process(self, config: MCPServerConfig) -> ValidationResult:
    ...
```

**Why?** Enables using class names before they're defined and the `X | Y` union syntax.

### Union Types (Python 3.10+)

```python
# Modern syntax (preferred)
path: Path | None = None
expires_at: datetime | None

# Old syntax (avoid)
from typing import Optional, Union
path: Optional[Path]  # Same as Path | None
```

### Type Hints for Collections

```python
# Built-in generics (Python 3.9+)
servers: dict[str, MCPServerConfig] = {}
args: list[str] = []
searched_paths: list[Path] = []

# Nested types
user_info: dict[str, str] = field(default_factory=dict)
```

### TYPE_CHECKING Guard

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # These imports only run during type checking, not at runtime
    # Avoids circular imports!
    from mcp_health.config.models import MCPServerConfig
```

**When to use:** When you need a type for annotations but importing it would cause circular imports.

---

## 2. Dataclasses & Pydantic Models

### Dataclasses with Defaults and Factories

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class ValidationResult:
    # Required fields (no default)
    status: TokenStatus
    message: str
    
    # Optional fields with defaults
    expires_at: datetime | None = None
    can_refresh: bool = False
    
    # Mutable defaults MUST use field(default_factory=...)
    user_info: dict[str, str] = field(default_factory=dict)
    scopes: list[str] = field(default_factory=list)
```

⚠️ **Critical Rule:** Never use mutable defaults directly (`= {}` or `= []`). They're shared across instances!

### Pydantic for Validation

```python
from pydantic import BaseModel, Field

class MCPServerConfig(BaseModel):
    command: str = Field(..., description="Command to execute")  # ... means required
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    
    # Helper methods on models
    def get_env_var(self, key: str, default: str | None = None) -> str | None:
        return self.env.get(key, default)
```

### Pydantic Field Aliases

```python
class MCPConfig(BaseModel):
    # JSON uses "mcpServers", Python uses "mcp_servers"
    mcp_servers: dict[str, MCPServerConfig] = Field(..., alias="mcpServers")
    
    model_config = {"populate_by_name": True}  # Allow both names
```

### Making Models Iterable

```python
class MCPConfig(BaseModel):
    mcp_servers: dict[str, MCPServerConfig]
    
    def __iter__(self):
        """Iterate over (name, config) pairs."""
        return iter(self.mcp_servers.items())
    
    def __len__(self) -> int:
        return len(self.mcp_servers)

# Usage:
for server_name, config in mcp_config:
    print(server_name)
```

---

## 3. Abstract Base Classes & Protocols

### Abstract Base Class Pattern

```python
from abc import ABC, abstractmethod

class BaseValidator(ABC):
    """Abstract base - cannot be instantiated directly."""
    
    service_name: str = "unknown"  # Class attribute with default
    
    @abstractmethod
    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Subclasses MUST implement this."""
        pass
    
    # Non-abstract methods provide shared behavior
    def extract_token(self, config: MCPServerConfig) -> str | None:
        env_var = self.get_token_env_var()
        if env_var:
            return config.get_env_var(env_var)
        return None
```

### Concrete Implementation

```python
class GitHubValidator(BaseValidator):
    service_name = "github"  # Override class attribute
    
    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        # Must implement abstract method
        token = self.extract_token(config)  # Use inherited method
        ...
```

---

## 4. Enum Patterns

### Enum with Helper Methods

```python
from enum import Enum

class TokenStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    MISSING = "missing"
    
    def is_healthy(self) -> bool:
        """Enum can have methods!"""
        return self == TokenStatus.VALID
    
    def needs_refresh(self) -> bool:
        return self in (TokenStatus.INVALID, TokenStatus.EXPIRED)
```

### Enum with Display Helpers

```python
class OverallStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

    def get_color(self) -> str:
        colors = {
            OverallStatus.HEALTHY: "green",
            OverallStatus.DEGRADED: "yellow",
            OverallStatus.UNHEALTHY: "red",
        }
        return colors.get(self, "white")
    
    def get_symbol(self) -> str:
        return {"HEALTHY": "✓", "DEGRADED": "⚠", "UNHEALTHY": "✗"}.get(self.name, "?")
```

---

## 5. Async/Await Patterns

### Basic Async Function

```python
import httpx

async def validate(self, config: MCPServerConfig) -> ValidationResult:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get("https://api.github.com/user", headers=headers)
        return self._handle_response(response)
```

### Running Async from Sync (CLI)

```python
import asyncio

@click.command()
def check():
    """Sync CLI command that runs async code."""
    asyncio.run(run_health_check())

async def run_health_check():
    """The actual async implementation."""
    result = await validator.validate(config)
```

### Async Context Manager

```python
async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
    # client is automatically closed after block
    response = await client.get(url)
```

---

## 6. Context Managers

### Suppressing Exceptions

```python
import contextlib

# Instead of:
try:
    data = json.loads(file.read_text())
except (json.JSONDecodeError, OSError):
    pass

# Use:
with contextlib.suppress(json.JSONDecodeError, OSError):
    data = json.loads(file.read_text())
```

---

## 7. Exception Handling

### Custom Exception Hierarchy

```python
class ConfigError(Exception):
    """Base exception for configuration errors."""
    pass

class ConfigNotFoundError(ConfigError):
    """Specific error with rich context."""
    def __init__(self, path: Path | None = None, searched_paths: list[Path] | None = None):
        self.path = path
        self.searched_paths = searched_paths or []
        message = self._build_message()
        super().__init__(message)
    
    def _build_message(self) -> str:
        if self.path:
            return f"Configuration file not found: {self.path}"
        paths_str = ", ".join(str(p) for p in self.searched_paths)
        return f"Configuration file not found. Searched: {paths_str}"
```

### Exception Chaining (PEP 3134)

```python
try:
    data = json.loads(content)
except json.JSONDecodeError as e:
    # "from e" chains exceptions - preserves original traceback
    raise ConfigParseError(path, str(e)) from e

# In CLI:
except ConfigError as e:
    console.print(f"Error: {e}")
    raise SystemExit(1) from e  # B904: Always chain in except blocks
```

---

## 8. Path Operations with pathlib

### Modern Path Usage

```python
from pathlib import Path

# Creating paths
home = Path.home()
config_path = home / ".cursor" / "mcp.json"  # Use / operator

# Checking existence
if config_path.exists():
    if config_path.is_file():
        content = config_path.read_text(encoding="utf-8")

# Iterating directories
for subdir in config_dir.iterdir():
    if subdir.is_dir():
        token_file = subdir / "tokens.json"

# Creating directories
token_dir.mkdir(parents=True, exist_ok=True)
```

---

## 9. Testing Patterns

### Pytest Fixtures

```python
import pytest

@pytest.fixture
def validator() -> GitHubValidator:
    """Create a fresh validator for each test."""
    return GitHubValidator()

@pytest.fixture
def github_config() -> MCPServerConfig:
    """Reusable test configuration."""
    return MCPServerConfig(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_testtoken"},
    )
```

### Fixtures with Dependencies

```python
@pytest.fixture
def atlassian_config(self, mock_atlassian_tokens: Path) -> MCPServerConfig:
    """Fixture that depends on another fixture."""
    return MCPServerConfig(
        command="npx",
        args=["-y", "mcp-remote@0.1.30"],
        env={"MCP_REMOTE_CONFIG_DIR": str(mock_atlassian_tokens)},
    )
```

### Async Test Marking

```python
@pytest.mark.asyncio
async def test_valid_token(self, validator, config):
    result = await validator.validate(config)
    assert result.status == TokenStatus.VALID
```

### Mocking HTTP with respx

```python
import respx
import httpx

@pytest.mark.asyncio
@respx.mock
async def test_github_api(self, validator, config):
    # Mock the API response
    respx.get("https://api.github.com/user").mock(
        return_value=httpx.Response(200, json={"login": "testuser"})
    )
    
    result = await validator.validate(config)
    assert result.status == TokenStatus.VALID
```

### Temporary Files in Tests

```python
@pytest.fixture
def temp_config_file(tmp_path: Path, sample_config: dict) -> Path:
    """tmp_path is a built-in pytest fixture."""
    config_path = tmp_path / "mcp.json"
    config_path.write_text(json.dumps(sample_config))
    return config_path
```

### Test Class Organization

```python
class TestGitHubValidator:
    """Group related tests in a class."""
    
    @pytest.fixture
    def validator(self) -> GitHubValidator:
        return GitHubValidator()
    
    def test_service_name(self, validator):
        """Self-contained fixtures for each test."""
        assert validator.service_name == "github"
```

---

## 10. CLI with Click

### Command Groups

```python
import click

@click.group()
@click.version_option(version="0.1.0")
def main():
    """MCP Health Check - Monitor your MCP server connections."""
    pass

@main.command()  # Subcommand of main
@click.option("--config", "-c", type=click.Path(exists=True, path_type=Path))
@click.option("--format", "-f", type=click.Choice(["console", "json"]), default="console")
@click.option("--verbose", "-v", is_flag=True)
def check(config: Path | None, format: str, verbose: bool):
    """Run health check on all MCP servers."""
    asyncio.run(run_health_check(config, format, verbose))
```

### Click Path Type

```python
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),  # Validates and converts to Path
)
```

---

## 11. Rich Console Output

### Tables and Panels

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

# Styled text
text = Text("Status OK")
text.stylize("bold green")

# Panel (boxed content)
console.print(Panel(text, expand=False))

# Table
table = Table(show_header=True, header_style="bold")
table.add_column("Server", style="cyan")
table.add_column("Status")
table.add_row("github", "✓ Valid")
console.print(table)
```

### Rich Markup

```python
console.print("[red]Error:[/] Something went wrong")
console.print("[bold cyan]Server:[/] github")
console.print("[yellow]Warning[/]: Token expires soon")
```

---

## 12. Walrus Operator & Modern Syntax

### Walrus Operator `:=`

```python
# Assign and use in one expression
if (token := config.get_env_var("TOKEN")) is None:
    return ValidationResult(status=TokenStatus.MISSING, ...)

# Using the assigned value
result = validate(token)
```

### f-strings with Expressions

```python
# Complex expressions in f-strings
message = f"Authenticated as {data.get('login', 'unknown')}"
error_msg = f"API error: {response.status_code} - {response.text[:100]}"
```

### Dictionary Get with Default

```python
# Safe dictionary access
login = data.get("login", "unknown")
scopes = headers.get("X-OAuth-Scopes", "").split(", ")
```

### Properties as Computed Attributes

```python
@dataclass
class ServerHealth:
    name: str
    token_result: ValidationResult | None = None
    
    @property
    def is_healthy(self) -> bool:
        """Computed on access, not stored."""
        return self.token_result is None or self.token_result.is_healthy()
    
    @property
    def status(self) -> OverallStatus:
        """Derive status from other attributes."""
        if self.is_healthy:
            return OverallStatus.HEALTHY
        return OverallStatus.UNHEALTHY
```

---

## Quick Reference Card

| Pattern | Example | Use Case |
|---------|---------|----------|
| Union types | `Path \| None` | Optional values |
| Field factory | `field(default_factory=dict)` | Mutable defaults |
| Walrus | `if (x := get_x()):` | Assign + check |
| Path ops | `home / ".config" / "app"` | Path building |
| Enum methods | `status.is_healthy()` | Rich enums |
| ABC | `@abstractmethod` | Interface contracts |
| Exception chain | `raise X from e` | Preserve context |
| respx mock | `@respx.mock` | HTTP testing |
| Rich markup | `[bold red]Error[/]` | Styled output |
| TYPE_CHECKING | `if TYPE_CHECKING:` | Avoid circular imports |

---

## Recommended Reading

1. **PEP 484** - Type Hints
2. **PEP 563** - Postponed Evaluation of Annotations
3. **PEP 557** - Data Classes
4. **PEP 3134** - Exception Chaining
5. **Click Documentation** - https://click.palletsprojects.com/
6. **Rich Documentation** - https://rich.readthedocs.io/
7. **Pydantic Documentation** - https://docs.pydantic.dev/

