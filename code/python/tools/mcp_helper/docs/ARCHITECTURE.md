# MCP Health Check Tool - Architecture

## Overview

The MCP Health Check Tool is a Python CLI application designed to monitor and validate MCP (Model Context Protocol) server connections. It provides token validation, connection testing, and automated/manual token refresh capabilities.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLI Layer                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  main.py → click commands (check, status, refresh)          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Core Layer                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ ConfigLoader │  │ HealthChecker│  │  ReportGenerator     │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐
│ Token Validators│ │ MCP Protocol    │ │ Token Refresh           │
│ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌───────────────────┐   │
│ │GitHubValid. │ │ │ │ MCPClient   │ │ │ │ OAuthRefresher    │   │
│ │SlackValid.  │ │ │ │ ServerSpawn │ │ │ │ UserNotifier      │   │
│ │AtlassianV.  │ │ │ └─────────────┘ │ │ └───────────────────┘   │
│ └─────────────┘ │ └─────────────────┘ └─────────────────────────┘
└─────────────────┘
```

## Component Details

### 1. CLI Layer (`cli.py`)

The entry point using Click framework:

```python
@click.group()
def main():
    """MCP Health Check CLI"""
    pass

@main.command()
@click.option('--config', '-c', help='Path to MCP config file')
@click.option('--format', type=click.Choice(['console', 'json']))
def check(config, format):
    """Run health check on all MCP servers"""
```

**Responsibilities:**
- Parse command-line arguments
- Coordinate between components
- Display results to user

### 2. Config Layer (`config/`)

#### `models.py` - Data Models

```python
class MCPServerConfig(BaseModel):
    command: str
    args: list[str]
    env: dict[str, str] = {}

class MCPConfig(BaseModel):
    mcp_servers: dict[str, MCPServerConfig]
```

#### `loader.py` - Configuration Loading

```python
class ConfigLoader:
    def load(self, path: Path | None = None) -> MCPConfig:
        """Load and validate MCP configuration"""
    
    def find_config(self) -> Path:
        """Find config in default locations"""
```

**Config Resolution Order:**
1. Explicit `--config` path
2. `~/.cursor/mcp.json`
3. `MCP_CONFIG_PATH` environment variable

### 3. Validators Layer (`validators/`)

#### `base.py` - Base Interface

```python
class TokenStatus(Enum):
    VALID = "valid"
    INVALID = "invalid"
    EXPIRED = "expired"
    MISSING = "missing"
    UNKNOWN = "unknown"

@dataclass
class ValidationResult:
    status: TokenStatus
    message: str
    expires_at: datetime | None = None
    can_refresh: bool = False
    refresh_instructions: str | None = None

class BaseValidator(ABC):
    @abstractmethod
    async def validate(self, config: MCPServerConfig) -> ValidationResult:
        """Validate token for this service"""
```

#### Service-Specific Validators

| Validator | Endpoint | Token Location |
|-----------|----------|----------------|
| `GitHubValidator` | `GET https://api.github.com/user` | `env.GITHUB_PERSONAL_ACCESS_TOKEN` |
| `SlackValidator` | `POST https://slack.com/api/auth.test` | `env.SLACK_BOT_TOKEN` |
| `AtlassianValidator` | `GET https://api.atlassian.com/me` | `MCP_REMOTE_CONFIG_DIR` token file |

### 4. MCP Protocol Layer (`mcp/`)

#### `spawner.py` - Server Process Management

```python
class ServerSpawner:
    async def spawn(self, config: MCPServerConfig) -> MCPConnection:
        """Spawn MCP server subprocess"""
    
    async def terminate(self, connection: MCPConnection) -> None:
        """Clean up server process"""
```

#### `client.py` - MCP Protocol Client

```python
class MCPClient:
    async def initialize(self, connection: MCPConnection) -> bool:
        """Send initialize request"""
    
    async def list_resources(self, connection: MCPConnection) -> list[Resource]:
        """List available resources to verify connection"""
    
    async def health_check(self, config: MCPServerConfig) -> ConnectionStatus:
        """Full health check: spawn → initialize → list_resources"""
```

**MCP Protocol Flow:**
```
Client                    Server
  │                         │
  │── initialize ──────────>│
  │<─── initializeResult ───│
  │                         │
  │── resources/list ──────>│
  │<─── resources ──────────│
  │                         │
  │── shutdown ────────────>│
  │                         │
```

### 5. Refresh Layer (`refresh/`)

#### `oauth.py` - OAuth Token Refresh

```python
class OAuthRefresher:
    async def refresh_atlassian(self, config_dir: Path) -> RefreshResult:
        """Refresh Atlassian OAuth token using stored refresh_token"""
```

**Atlassian OAuth Flow:**
1. Read `tokens.json` from `MCP_REMOTE_CONFIG_DIR`
2. Extract `refresh_token`
3. POST to `https://auth.atlassian.com/oauth/token`
4. Store new `access_token` and `refresh_token`

#### `notifier.py` - User Notification

```python
class UserNotifier:
    def notify_github_refresh(self) -> str:
        """Return instructions for GitHub PAT regeneration"""
    
    def notify_slack_refresh(self) -> str:
        """Return instructions for Slack bot token regeneration"""
```

### 6. Reporting Layer (`reporting/`)

```python
class HealthReport:
    servers: dict[str, ServerHealth]
    timestamp: datetime
    overall_status: OverallStatus

class ReportGenerator:
    def generate_console(self, report: HealthReport) -> None:
        """Rich console output with colors"""
    
    def generate_json(self, report: HealthReport) -> str:
        """JSON output for automation"""
```

## Data Flow

```
1. User runs: mcp-health check

2. ConfigLoader.load()
   └── Parse JSON → MCPConfig

3. For each server in MCPConfig:
   │
   ├── Validator.validate(config)
   │   └── API call → TokenStatus
   │
   ├── If TokenStatus.INVALID:
   │   ├── OAuthRefresher (if OAuth)
   │   └── UserNotifier (if PAT)
   │
   └── MCPClient.health_check(config)
       └── Spawn → Initialize → List → ConnectionStatus

4. ReportGenerator.generate(results)
   └── Console/JSON output
```

## Error Handling Strategy

| Error Type | Handling |
|------------|----------|
| Network timeout | Retry with backoff, report as degraded |
| Invalid token | Mark invalid, trigger refresh/notify |
| Config parse error | Fail fast with clear message |
| MCP spawn failure | Report as unhealthy, include stderr |
| MCP protocol error | Parse error, report specific issue |

## Testing Strategy

See [TEST_PLAN.md](TEST_PLAN.md) for detailed testing approach.

## Future Extensibility

1. **New Services**: Add new validator in `validators/`
2. **New Refresh Methods**: Extend `refresh/` module
3. **New Output Formats**: Add to `ReportGenerator`
4. **Metrics Export**: Add Prometheus/StatsD integration

