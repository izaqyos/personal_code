# Manual Test Plan: MCP Health Check Smoke Tests

This document provides step-by-step smoke tests to manually verify the MCP Health Check Tool functionality.

---

## Prerequisites

```bash
# Navigate to project
cd /Users/yosii/work/git/personal_code/code/python/tools/mcp_helper

# Activate virtual environment
source .venv/bin/activate

# Verify installation
mcp-health --version
# Expected: mcp-health, version 0.1.0
```

---

## Test 1: Basic Health Check (No Config)

**Purpose:** Verify tool handles missing config gracefully.

```bash
# Remove or rename existing config temporarily
mv ~/.cursor/mcp.json ~/.cursor/mcp.json.bak 2>/dev/null

mcp-health check
```

**Expected Output:**
```
Error loading config: Configuration file not found. Searched: ~/.cursor/mcp.json
```

**Exit Code:** `1`

```bash
# Restore config
mv ~/.cursor/mcp.json.bak ~/.cursor/mcp.json 2>/dev/null
```

---

## Test 2: List Configured Servers

**Purpose:** Verify tool can read and display MCP configuration.

```bash
mcp-health list-servers
```

**Expected Output:**
```
Configured MCP Servers:

  github
    Command: npx
    Args: -y @modelcontextprotocol/server-github
    Env vars: GITHUB_PERSONAL_ACCESS_TOKEN

  perimeter81-atlassian
    Command: npx
    Args: -y mcp-remote@0.1.30 https://mcp.atlassian.com/v1/sse
    Env vars: MCP_REMOTE_CONFIG_DIR

  slack
    Command: npx
    Args: -y @modelcontextprotocol/server-slack
    Env vars: SLACK_BOT_TOKEN, SLACK_TEAM_ID
```

**Exit Code:** `0`

---

## Test 3: Health Check with Valid Tokens

**Purpose:** Verify health check validates tokens correctly.

```bash
mcp-health check --skip-mcp
```

**Expected Output (if tokens are valid):**
```
╭──────────────────────────────────────────────────╮
│ MCP Server Health Check (3/3)                     │
╰──────────────────────────────────────────────────╯

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Server                ┃ Token Status  ┃ Connection   ┃ Action Required ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ github                │ ✓ Valid       │ Not tested   │                 │
│ perimeter81-atlassian │ ✓ Valid       │ Not tested   │                 │
│ slack                 │ ✓ Valid       │ Not tested   │                 │
└───────────────────────┴───────────────┴──────────────┴─────────────────┘
```

**Exit Code:** `0` (healthy), `1` (unhealthy)

---

## Test 4: Verbose Output

**Purpose:** Verify verbose mode shows additional details.

```bash
mcp-health check --skip-mcp --verbose
```

**Expected Output:** Same table plus additional details section:
```
Detailed Results:

github:
  Token: Authenticated as <username>
    login: <username>
    name: <your name>
    email: <your email>

perimeter81-atlassian:
  Token: Atlassian OAuth token is valid
    ...
```

---

## Test 5: JSON Output

**Purpose:** Verify JSON output format for scripting.

```bash
mcp-health check --skip-mcp --format json
```

**Expected Output (parseable JSON):**
```json
{
  "timestamp": "2026-01-05T...",
  "config_path": null,
  "overall_status": "healthy",
  "healthy_count": 3,
  "total_count": 3,
  "servers": {
    "github": {
      "status": "healthy",
      "is_healthy": true,
      "token": {
        "status": "valid",
        "message": "Authenticated as ...",
        "can_refresh": false,
        "user_info": {}
      }
    },
    ...
  }
}
```

**Validation:**
```bash
# Verify it's valid JSON
mcp-health check --skip-mcp --format json | python -m json.tool > /dev/null && echo "✓ Valid JSON"
```

---

## Test 6: Custom Config Path

**Purpose:** Verify tool accepts custom config location.

```bash
# Create a test config
cat > /tmp/test-mcp.json << 'EOF'
{
  "mcpServers": {
    "test-server": {
      "command": "echo",
      "args": ["test"]
    }
  }
}
EOF

mcp-health list-servers --config /tmp/test-mcp.json
```

**Expected Output:**
```
Configured MCP Servers:

  test-server
    Command: echo
    Args: test
```

---

## Test 7: Refresh Command (Manual Token)

**Purpose:** Verify refresh command shows instructions for non-OAuth tokens.

```bash
mcp-health refresh github
```

**Expected Output:**
```
github uses a non-refreshable token.

To refresh your GitHub Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Generate a new token with required permissions
3. Update your MCP configuration with the new token
...
```

---

## Test 8: Invalid Token Handling

**Purpose:** Verify tool correctly detects invalid tokens.

```bash
# Create config with invalid token
cat > /tmp/invalid-mcp.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_invalid_token_12345"
      }
    }
  }
}
EOF

mcp-health check --config /tmp/invalid-mcp.json --skip-mcp
```

**Expected Output:**
```
┏━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Server ┃ Token Status ┃ Connection   ┃ Action Required                   ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ github │ ✗ Invalid    │ Not tested   │ Regenerate GitHub PAT             │
└────────┴──────────────┴──────────────┴───────────────────────────────────┘

Actions Required:
  • github: Regenerate GitHub PAT
```

**Exit Code:** `1`

---

## Test 9: Missing Token Detection

**Purpose:** Verify tool detects missing tokens.

```bash
cat > /tmp/missing-token.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {}
    }
  }
}
EOF

mcp-health check --config /tmp/missing-token.json --skip-mcp
```

**Expected Output:**
```
│ github │ ✗ Missing    │ Not tested   │ ...                               │
```

---

## Test 10: Atlassian OAuth Check

**Purpose:** Verify Atlassian token validation works.

```bash
mcp-health check --skip-mcp 2>&1 | grep -i atlassian
```

**Expected:** Shows Atlassian status (Valid, Expired, or Missing based on your actual tokens).

---

## Smoke Test Summary Checklist

Run through this checklist to verify basic functionality:

| # | Test | Command | Expected Exit |
|---|------|---------|---------------|
| 1 | Missing config | `mcp-health check` (no config) | 1 |
| 2 | List servers | `mcp-health list-servers` | 0 |
| 3 | Basic check | `mcp-health check --skip-mcp` | 0 or 1 |
| 4 | Verbose | `mcp-health check --skip-mcp -v` | 0 or 1 |
| 5 | JSON output | `mcp-health check --skip-mcp -f json` | 0 or 1 |
| 6 | Custom config | `mcp-health list-servers -c /path` | 0 |
| 7 | Refresh help | `mcp-health refresh github` | 0 |
| 8 | Invalid token | (with bad config) | 1 |
| 9 | Missing token | (with empty env) | 1 |
| 10 | Version | `mcp-health --version` | 0 |

---

## Cleanup

```bash
# Remove test files
rm -f /tmp/test-mcp.json /tmp/invalid-mcp.json /tmp/missing-token.json
```

---

## Troubleshooting Common Issues

### Tool not found
```bash
# Ensure venv is activated
source .venv/bin/activate

# Reinstall
pip install -e ".[dev]"
```

### Network errors during validation
```bash
# Check internet connectivity
curl -I https://api.github.com

# Run with skip-mcp to avoid spawning servers
mcp-health check --skip-mcp
```

### Atlassian token issues
```bash
# Check token file exists
ls -la ~/.mcp-auth/mcp-remote-stable/tokens.json

# Verify token content
cat ~/.mcp-auth/mcp-remote-stable/tokens.json | python -m json.tool
```

