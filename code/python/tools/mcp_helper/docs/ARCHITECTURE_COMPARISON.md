# MCP Client Architecture Comparison

## Executive Summary

This document compares how different AI coding assistants handle Atlassian MCP authentication, explaining why Claude Code works seamlessly while Cursor requires workarounds.

## Architecture Overview

### Claude Code (Anthropic Desktop App)

```
┌─────────────────┐
│   Claude Code   │
│                 │
│  ┌───────────┐  │
│  │Native MCP │  │
│  │OAuth 2.1  │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │ HTTPS/SSE
         │ Direct Connection
         ▼
┌─────────────────────────┐
│  mcp.atlassian.com/v1   │
│  (Atlassian Cloud)      │
└─────────────────────────┘
```

**Characteristics:**
- ✅ Native OAuth 2.1 support built into the application
- ✅ Direct HTTPS/SSE connection to Atlassian cloud
- ✅ Token management handled internally by Anthropic
- ✅ Seamless token refresh without user intervention
- ✅ No external processes or file synchronization
- ✅ Secure token storage within application

**Token Storage:**
- Managed by Anthropic's infrastructure
- Not exposed to user filesystem
- Automatic refresh and rotation

### Cursor (Desktop IDE)

```
┌─────────────────┐
│     Cursor      │
│                 │
│  ┌───────────┐  │
│  │stdio MCP  │  │
│  │Client     │  │
│  └─────┬─────┘  │
└────────┼────────┘
         │ stdio (local)
         ▼
┌─────────────────────────┐
│      mcp-remote         │
│   (Local Proxy)         │
│                         │
│  ┌──────────────────┐   │
│  │ OAuth Handler    │   │
│  │ (Browser-based)  │   │
│  └──────────────────┘   │
│                         │
│  ┌──────────────────┐   │
│  │ Token Storage    │   │
│  │ ~/.mcp-auth/     │   │
│  └──────────────────┘   │
└────────┬────────────────┘
         │ HTTPS/SSE
         │ Proxied Connection
         ▼
┌─────────────────────────┐
│  mcp.atlassian.com/v1   │
│  (Atlassian Cloud)      │
└─────────────────────────┘
```

**Characteristics:**
- ⚠️ Requires external `mcp-remote` proxy process
- ⚠️ stdio-only MCP support (no native SSE)
- ⚠️ Browser-based OAuth flow (external)
- ⚠️ Token files stored on local filesystem
- ⚠️ Token file synchronization issues
- ⚠️ Manual re-authentication via toggle

**Token Storage:**
- Local files: `~/.mcp-auth/mcp-remote-stable/mcp-remote-0.1.30/`
- Hash-prefixed filenames: `<hash>_tokens.json`
- Can become stale while in-memory tokens are fresh

## Why mcp-remote is Required

### MCP Transport Mechanisms

The Model Context Protocol supports two primary transports:

1. **stdio** (Standard Input/Output)
   - For local processes
   - Simple pipe-based communication
   - No authentication required
   - Supported by all desktop IDEs

2. **SSE** (Server-Sent Events)
   - For remote servers over HTTP
   - Requires HTTP connection management
   - Supports OAuth authentication
   - Not natively supported by most IDEs

### The Gap

**Problem:** Atlassian MCP server uses **SSE + OAuth 2.1**, but Cursor only supports **stdio**.

**Solution:** `mcp-remote` acts as a bridge:
- Accepts stdio from Cursor
- Manages OAuth 2.1 flow via browser
- Maintains HTTP/SSE connection to Atlassian
- Proxies MCP messages bidirectionally
- Stores tokens locally for subsequent connections

### Why No Alternative Exists

`mcp-remote` is the **official Atlassian-recommended solution** for desktop clients. From the [official Atlassian MCP Server repository](https://github.com/atlassian/atlassian-mcp-server):

> "Desktop Setup for Local Clients: A supported IDE (for example, Claude desktop, VS Code, or Cursor) or a custom MCP-compatible client. Node.js v18+ installed to run the local MCP proxy (mcp-remote)."

**No alternative exists because:**
1. Atlassian's MCP server only supports SSE transport
2. Desktop IDEs only support stdio transport
3. `mcp-remote` is the official bridge
4. No other proxy tool implements this functionality

## Token Management Comparison

### Claude Code

```python
# Pseudocode representation
class ClaudeCodeMCPClient:
    def __init__(self):
        self.oauth_handler = NativeOAuthHandler()
        self.token_store = SecureInternalStorage()
    
    def connect_atlassian(self):
        # Native OAuth flow within application
        tokens = self.oauth_handler.authenticate()
        self.token_store.save(tokens)
        
        # Direct SSE connection
        self.connection = SSEConnection(
            url="https://mcp.atlassian.com/v1/sse",
            auth=BearerToken(tokens.access_token)
        )
    
    def refresh_token(self):
        # Automatic background refresh
        new_tokens = self.oauth_handler.refresh(
            self.token_store.get_refresh_token()
        )
        self.token_store.save(new_tokens)
        # No user intervention needed
```

### Cursor + mcp-remote

```python
# Pseudocode representation
class CursorMCPClient:
    def __init__(self):
        self.process = subprocess.Popen(
            ["npx", "mcp-remote", "https://mcp.atlassian.com/v1/sse"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
    
    def connect_atlassian(self):
        # mcp-remote handles OAuth externally
        # 1. Opens browser for user authentication
        # 2. Stores tokens in ~/.mcp-auth/
        # 3. Keeps tokens in memory
        # 4. May not persist immediately
        
        # stdio communication with proxy
        self.send_mcp_request(self.process.stdin)
        response = self.read_mcp_response(self.process.stdout)

class MCPRemoteProxy:
    def __init__(self):
        self.token_file = Path("~/.mcp-auth/.../tokens.json")
        self.tokens_in_memory = None
    
    def load_tokens(self):
        if self.token_file.exists():
            self.tokens_in_memory = json.loads(
                self.token_file.read_text()
            )
    
    def refresh_token(self):
        # Refresh in memory
        new_tokens = oauth_refresh(self.tokens_in_memory)
        self.tokens_in_memory = new_tokens
        
        # May not persist immediately to disk
        # File becomes stale!
```

## Performance Comparison

| Aspect | Claude Code | Cursor + mcp-remote |
|--------|-------------|---------------------|
| **Initial Setup** | Seamless (in-app) | Manual (browser) |
| **Token Refresh** | Automatic | Manual toggle |
| **Connection Latency** | Low (direct) | Higher (proxied) |
| **Token Validation** | Native | File-based (unreliable) |
| **Error Recovery** | Automatic | Manual |
| **Process Overhead** | None | Extra Node.js process |
| **Memory Usage** | Integrated | +50-100MB for proxy |

## Security Comparison

### Claude Code

**Advantages:**
- ✅ Tokens stored in secure application storage
- ✅ No exposure to filesystem
- ✅ Automatic rotation
- ✅ Centralized security updates

**Disadvantages:**
- ⚠️ Proprietary (trust Anthropic)
- ⚠️ No user control over token storage

### Cursor + mcp-remote

**Advantages:**
- ✅ Open source (mcp-remote)
- ✅ User control over token files
- ✅ Can inspect/debug tokens

**Disadvantages:**
- ⚠️ Tokens in plain text on filesystem
- ⚠️ No OS keychain integration
- ⚠️ File permissions must be managed manually
- ⚠️ Tokens can be accidentally committed to git

## Recommendations

### For Individual Developers

**Use Claude Code if:**
- Heavy Jira/Confluence usage
- Want seamless experience
- Don't need IDE-specific features

**Use Cursor if:**
- Need AI-first IDE features
- Willing to manage token issues
- Can toggle MCP when needed

**Hybrid Approach:**
- Use Claude Code for Atlassian tasks
- Use Cursor for coding tasks
- Run `mcp-health` to monitor Cursor tokens

### For Teams

**Standardize on:**
1. **Claude Code** for Atlassian-heavy teams
2. **Document workarounds** if using Cursor
3. **Monitor with mcp-health** in CI/CD
4. **File issues** with mcp-remote and Cursor teams

### For Tool Developers

**Best Practices:**
1. **Implement native OAuth** - Don't rely on external proxies
2. **Support SSE transport** - Enable direct remote connections
3. **Use OS credential storage** - Keychain/Credential Manager
4. **Provide health checks** - Built-in token validation
5. **Document architecture** - Clear OAuth flow explanation

## Future Outlook

### Short-term (2025)

**Expected:**
- VS Code native MCP support improvements
- Cursor may add native MCP OAuth
- `mcp-remote` token persistence fixes

**Recommendations:**
- Continue using workarounds
- Monitor IDE updates
- Contribute to mcp-remote

### Medium-term (2026)

**Possible:**
- Standardized MCP OAuth protocol
- IDE-native token management
- Elimination of proxy requirement

**Prepare:**
- Document current issues
- Build migration plans
- Test new features early

### Long-term (2027+)

**Vision:**
- All IDEs support native MCP OAuth
- Standardized token storage
- Seamless multi-server management

## References

- [Official Atlassian MCP Server](https://github.com/atlassian/atlassian-mcp-server)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [mcp-remote Repository](https://github.com/modelcontextprotocol/mcp-remote)
- [Atlassian OAuth 2.1 Documentation](https://developer.atlassian.com/cloud/oauth/getting-started/)
- [mcp-health Tool](../README.md)

## Conclusion

**Claude Code's seamless experience** comes from native MCP OAuth support and direct cloud connection. **Cursor's token issues** stem from the architectural requirement for `mcp-remote` as a proxy, which introduces token file synchronization challenges.

**There is no alternative to mcp-remote** for desktop IDEs that only support stdio transport. The solution is either:
1. Use Claude Code for Atlassian tasks
2. Accept the limitations and use workarounds
3. Wait for Cursor to add native MCP OAuth support

The `mcp-health` tool provides the best possible monitoring and recovery for Cursor users, but cannot eliminate the fundamental architectural limitations.

