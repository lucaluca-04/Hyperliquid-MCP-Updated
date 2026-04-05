# Hyperliquid MCP Updated

Read-only [Model Context Protocol](https://modelcontextprotocol.io/) server for [Hyperliquid](https://hyperliquid.xyz/) using the official [`hyperliquid-python-sdk`](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) (see `pyproject.toml`). Use this when third-party MCP wrappers drift from the SDK.

## Features

- **No private key** — only public `POST /info` endpoints.
- **One MCP tool per `Info` HTTP method** (all read-only SDK methods that call `/info`), plus **`hl_info_request`** for any extra documented `type` not yet wrapped.
- **Not included**: WebSocket `subscribe` / `unsubscribe`, `Exchange` (signing / trading), and internal helpers like `set_perp_meta`.

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

## Tools ↔ `hyperliquid.info.Info` (SDK)

| MCP tool | SDK method |
|----------|------------|
| `hl_clearinghouse_state` | `user_state` |
| `hl_spot_clearinghouse_state` | `spot_user_state` |
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
| `hl_user_twap_slice_fills` | `user_twap_slice_fills` |
| `hl_user_fees` | `user_fees` |
| `hl_user_staking_summary` | `user_staking_summary` |
| `hl_user_staking_delegations` | `user_staking_delegations` |
| `hl_user_staking_rewards` | `user_staking_rewards` |
| `hl_delegator_history` | `delegator_history` |
| `hl_order_status_by_oid` | `query_order_by_oid` |
| `hl_order_status_by_cloid` | `query_order_by_cloid` |
| `hl_referral_state` | `query_referral_state` |
| `hl_sub_accounts` | `query_sub_accounts` |
| `hl_user_to_multi_sig_signers` | `query_user_to_multi_sig_signers` |
| `hl_perp_deploy_auction_status` | `query_perp_deploy_auction_status` |
| `hl_user_dex_abstraction` | `query_user_dex_abstraction_state` |
| `hl_user_abstraction` | `query_user_abstraction_state` |
| `hl_user_rate_limit` | `user_rate_limit` |
| `hl_spot_deploy_auction_status` | `query_spot_deploy_auction_status` |
| `hl_extra_agents` | `extra_agents` |
| `hl_meta` | `meta` |
| `hl_meta_and_asset_ctxs` | `meta_and_asset_ctxs` |
| `hl_perp_dexs` | `perp_dexs` |
| `hl_spot_meta` | `spot_meta` |
| `hl_spot_meta_and_asset_ctxs` | `spot_meta_and_asset_ctxs` |
| `hl_all_mids` | `all_mids` |
| `hl_l2_book` | `l2_snapshot` |
| `hl_candles` | `candles_snapshot` |
| `hl_funding_history` | `funding_history` |
| `hl_predicted_fundings` | *(no SDK method)* → `post(..., {"type":"predictedFundings"})` |
| `hl_active_asset_data` | *(no SDK method)* → `post(..., {"type":"activeAssetData", ...})` |
| `hl_info_request` | raw `post("/info", {**payload, "type": request_type})` |

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

## License

MIT
