# Hyperliquid MCP Updated

Read-only [Model Context Protocol](https://modelcontextprotocol.io/) server for [Hyperliquid](https://hyperliquid.xyz/) using the official [`hyperliquid-python-sdk`](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) (pinned compatible in `pyproject.toml`). Use this when third-party MCP wrappers drift from the SDK.

## Features

- **No private key** — only public `POST /info` endpoints.
- Tools match current SDK method names (`user_fills_by_time`, `user_funding_history`, `user_vault_equities`, etc.).
- **`hl_info_request`** — escape hatch for documented `type` + JSON body (e.g. vault APIs if exposed by Hyperliquid).

## Install

```bash
cd Hyperliquid-MCP-Updated
uv venv && source .venv/bin/activate   # or: python -m venv .venv
uv pip install -e .
```

Run (stdio, for MCP clients):

```bash
hyperliquid-mcp-updated
```

## Environment

| Variable | Meaning |
|----------|---------|
| `HL_TESTNET` | `true` / `1` → `https://api.hyperliquid-testnet.xyz` |
| `HL_API_URL` | Override base URL entirely |
| `HL_LOG_LEVEL` | Default `WARNING` |

## Cursor `mcp.json`

**Local checkout** (replace path):

```json
{
  "mcpServers": {
    "hyperliquid-updated": {
      "command": "/Users/you/path/to/Hyperliquid-MCP-Updated/.venv/bin/hyperliquid-mcp-updated",
      "args": [],
      "env": {}
    }
  }
}
```

Or with `uv` (no venv path hardcoded):

```json
{
  "mcpServers": {
    "hyperliquid-updated": {
      "command": "/Users/you/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/you/path/to/Hyperliquid-MCP-Updated",
        "run",
        "hyperliquid-mcp-updated"
      ],
      "env": {}
    }
  }
}
```

After editing, reload MCP in Cursor settings.

## Publish to GitHub

```bash
cd Hyperliquid-MCP-Updated
git init
git remote add origin https://github.com/lucaluca-04/Hyperliquid-MCP-Updated.git
git add .
git commit -m "Initial hyperliquid-mcp-updated server"
git branch -M main
git push -u origin main
```

## Tools (summary)

| Tool | SDK / API |
|------|-----------|
| `hl_clearinghouse_state` | `user_state` |
| `hl_open_orders` | `open_orders` |
| `hl_frontend_open_orders` | `frontend_open_orders` |
| `hl_user_fills` | `user_fills` |
| `hl_user_fills_by_time` | `user_fills_by_time` |
| `hl_user_funding_history` | `user_funding_history` |
| `hl_portfolio` | `portfolio` |
| `hl_user_vault_equities` | `user_vault_equities` |
| `hl_user_role` | `user_role` |
| `hl_user_non_funding_ledger_updates` | `user_non_funding_ledger_updates` |
| `hl_historical_orders` | `historical_orders` |
| `hl_meta` | `meta` |
| `hl_all_mids` | `all_mids` |
| `hl_l2_book` | `l2_snapshot` |
| `hl_candles` | `candles_snapshot` |
| `hl_funding_history` | `funding_history` |
| `hl_info_request` | raw `post("/info", ...)` |

Trading / signing is **not** included in this package.

## License

MIT
