"""MCP server: Hyperliquid read-only Info endpoints via hyperliquid-python-sdk."""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Any

from hyperliquid.info import Info
from hyperliquid.utils import constants
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "hyperliquid-mcp-updated",
    instructions=(
        "Hyperliquid Info API tools. All calls are read-only HTTP to Hyperliquid. "
        "Use hl_clearinghouse_state / hl_open_orders / hl_user_fills_by_time / "
        "hl_user_funding_history / hl_portfolio / hl_user_vault_equities for address research. "
        "Times are Unix milliseconds. No private key required."
    ),
)


def _base_url() -> str:
    if custom := os.environ.get("HL_API_URL", "").strip():
        return custom
    if os.environ.get("HL_TESTNET", "").lower() in ("1", "true", "yes"):
        return constants.TESTNET_API_URL
    return constants.MAINNET_API_URL


@lru_cache(maxsize=1)
def _info() -> Info:
    return Info(base_url=_base_url(), skip_ws=True)


def _json_text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


@mcp.tool()
def hl_clearinghouse_state(user: str, dex: str = "") -> str:
    """Perpetual clearinghouse state: positions, margin summary, withdrawable (clearinghouseState)."""
    return _json_text(_info().user_state(user, dex=dex))


@mcp.tool()
def hl_open_orders(user: str, dex: str = "") -> str:
    """Open resting orders for a user."""
    return _json_text(_info().open_orders(user, dex=dex))


@mcp.tool()
def hl_frontend_open_orders(user: str, dex: str = "") -> str:
    """Open orders including trigger/TPSL-style visibility (frontendOpenOrders)."""
    return _json_text(_info().frontend_open_orders(user, dex=dex))


@mcp.tool()
def hl_user_fills(user: str) -> str:
    """Recent user fills (bounded by API; use hl_user_fills_by_time for a window)."""
    return _json_text(_info().user_fills(user))


@mcp.tool()
def hl_user_fills_by_time(
    user: str,
    start_time_ms: int,
    end_time_ms: int | None = None,
    aggregate_by_time: bool = False,
) -> str:
    """User fills between start_time_ms and optional end_time_ms (userFillsByTime)."""
    return _json_text(
        _info().user_fills_by_time(
            user,
            start_time_ms,
            end_time=end_time_ms,
            aggregate_by_time=aggregate_by_time,
        )
    )


@mcp.tool()
def hl_user_funding_history(user: str, start_time_ms: int, end_time_ms: int | None = None) -> str:
    """User funding payments (userFunding)."""
    return _json_text(
        _info().user_funding_history(user, start_time_ms, endTime=end_time_ms)
    )


@mcp.tool()
def hl_portfolio(user: str) -> str:
    """Portfolio performance snapshot (account value / PnL history payloads)."""
    return _json_text(_info().portfolio(user))


@mcp.tool()
def hl_user_vault_equities(user: str) -> str:
    """User's equity across Hyperliquid vaults (userVaultEquities)."""
    return _json_text(_info().user_vault_equities(user))


@mcp.tool()
def hl_user_role(user: str) -> str:
    """Account role metadata (userRole)."""
    return _json_text(_info().user_role(user))


@mcp.tool()
def hl_user_non_funding_ledger_updates(
    user: str,
    start_time_ms: int,
    end_time_ms: int | None = None,
) -> str:
    """Non-funding ledger: deposits, transfers, liquidations, etc."""
    return _json_text(
        _info().user_non_funding_ledger_updates(
            user, start_time_ms, endTime=end_time_ms
        )
    )


@mcp.tool()
def hl_historical_orders(user: str) -> str:
    """Historical orders for user (historicalOrders)."""
    return _json_text(_info().historical_orders(user))


@mcp.tool()
def hl_meta(dex: str = "") -> str:
    """Perp metadata: universe, sz decimals (meta)."""
    return _json_text(_info().meta(dex=dex))


@mcp.tool()
def hl_all_mids(dex: str = "") -> str:
    """Mid prices for all assets (allMids)."""
    return _json_text(_info().all_mids(dex=dex))


@mcp.tool()
def hl_l2_book(coin: str) -> str:
    """L2 order book snapshot for a coin symbol (e.g. BTC, ETH)."""
    return _json_text(_info().l2_snapshot(coin))


@mcp.tool()
def hl_candles(coin: str, interval: str, start_time_ms: int, end_time_ms: int) -> str:
    """OHLCV candles: interval like 1m, 1h, 1d."""
    return _json_text(
        _info().candles_snapshot(coin, interval, start_time_ms, end_time_ms)
    )


@mcp.tool()
def hl_funding_history(coin: str, start_time_ms: int, end_time_ms: int | None = None) -> str:
    """Historical funding rates for a perp coin (not user-specific)."""
    return _json_text(_info().funding_history(coin, start_time_ms, endTime=end_time_ms))


@mcp.tool()
def hl_info_request(request_type: str, payload: str = "{}") -> str:
    """Advanced: raw POST /info. request_type maps to JSON \"type\" field; payload is JSON object merged in.

    Example: request_type=\"vaultDetails\", payload='{\"vaultAddress\": \"0x...\"}'
    Only use for types documented in Hyperliquid API; invalid types will error.
    """
    extra = json.loads(payload) if payload.strip() else {}
    if not isinstance(extra, dict):
        raise ValueError("payload must be a JSON object")
    body: dict[str, Any] = {**extra, "type": request_type}
    return _json_text(_info().post("/info", body))


def main() -> None:
    logging.basicConfig(level=os.environ.get("HL_LOG_LEVEL", "WARNING"))
    mcp.run()


if __name__ == "__main__":
    main()
