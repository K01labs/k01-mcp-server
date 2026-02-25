# Authentication

The K01 MCP server uses Bearer token authentication. Every request must include a valid API key.

## Getting an API Key

API keys are currently issued manually. Contact K01 at [k01.is](https://k01.is) to request access.

Self-service key provisioning is coming soon.

## Using Your API Key

Include the key as a Bearer token in the `Authorization` header. How you configure this depends on your MCP client.

### Claude Desktop

Edit your Claude Desktop MCP configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "k01": {
      "url": "https://mcp.k01.is/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

### Cursor

Add to `.cursor/mcp.json` in your project or global config:

```json
{
  "mcpServers": {
    "k01": {
      "url": "https://mcp.k01.is/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### Direct HTTP

If you're integrating directly via HTTP:

```bash
curl -X POST https://mcp.k01.is/mcp \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize"}'
```

## Security Notes

- Keep your API key confidential. Do not commit it to version control.
- API keys are scoped to your account and usage is tracked.
- If you suspect your key has been compromised, contact K01 immediately for a replacement.
- All traffic to the MCP endpoint is encrypted via TLS.
