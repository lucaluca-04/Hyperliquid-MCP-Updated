"""MCP server: Hyperliquid read-only Info endpoints via hyperliquid-python-sdk."""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from typing import Any

from hyperliquid.info import Info
from hyperliquid.utils import constants
from hyperliquid.utils.types import Cloid
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

mcp = FastMCP(
    "hyperliquid-mcp-updated",
    instructions=(
        "Hyperliquid Info API tools: one tool per hyperliquid.info.Info HTTP method "
        "(clearinghouse, fills, funding, portfolio, meta, spot, staking, orders, etc.) "
        "plus hl_info_request for raw POST /info. Read-only; times are Unix ms; no private key."
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
def hl_spot_clearinghouse_state(user: str) -> str:
    """Spot clearinghouse balances (spotClearinghouseState)."""
    return _json_text(_info().spot_user_state(user))


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
def hl_meta_and_asset_ctxs() -> str:
    """Perp meta plus per-asset mark/oracle/funding/OI context (metaAndAssetCtxs)."""
    return _json_text(_info().meta_and_asset_ctxs())


@mcp.tool()
def hl_perp_dexs() -> str:
    """List perp dex deployments (perpDexs)."""
    return _json_text(_info().perp_dexs())


@mcp.tool()
def hl_spot_meta() -> str:
    """Spot pair metadata (spotMeta)."""
    return _json_text(_info().spot_meta())


@mcp.tool()
def hl_spot_meta_and_asset_ctxs() -> str:
    """Spot meta plus asset contexts (spotMetaAndAssetCtxs)."""
    return _json_text(_info().spot_meta_and_asset_ctxs())


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
def hl_predicted_fundings() -> str:
    """Predicted funding across venues (HlPerp / BinPerp / BybitPerp) — same idea as Funding Comparison UI (predictedFundings)."""
    return _json_text(_info().post("/info", {"type": "predictedFundings"}))


@mcp.tool()
def hl_active_asset_data(user: str, coin: str) -> str:
    """Per-user per-coin leverage, max trade sizes, available to trade (activeAssetData). Official HTTP Info; SDK exposes mainly via WS."""
    return _json_text(_info().post("/info", {"type": "activeAssetData", "user": user, "coin": coin}))


@mcp.tool()
def hl_user_fees(user: str) -> str:
    """User fee tier and daily volume stats (userFees)."""
    return _json_text(_info().user_fees(user))


@mcp.tool()
def hl_user_staking_summary(user: str) -> str:
    """Staking summary for user (delegatorSummary)."""
    return _json_text(_info().user_staking_summary(user))


@mcp.tool()
def hl_user_staking_delegations(user: str) -> str:
    """Active staking delegations (delegations)."""
    return _json_text(_info().user_staking_delegations(user))


@mcp.tool()
def hl_user_staking_rewards(user: str) -> str:
    """Staking reward history (delegatorRewards)."""
    return _json_text(_info().user_staking_rewards(user))


@mcp.tool()
def hl_delegator_history(user: str) -> str:
    """Delegate / undelegate history (delegatorHistory)."""
    return _json_text(_info().delegator_history(user))


@mcp.tool()
def hl_order_status_by_oid(user: str, oid: int) -> str:
    """Order status by numeric order id (orderStatus)."""
    return _json_text(_info().query_order_by_oid(user, oid))


@mcp.tool()
def hl_order_status_by_cloid(user: str, cloid_hex: str) -> str:
    """Order status by client order id: 0x + 32 hex chars (16 bytes) (orderStatus)."""
    return _json_text(_info().query_order_by_cloid(user, Cloid.from_str(cloid_hex)))


@mcp.tool()
def hl_referral_state(user: str) -> str:
    """Referral program state (referral)."""
    return _json_text(_info().query_referral_state(user))


@mcp.tool()
def hl_sub_accounts(user: str) -> str:
    """Sub-accounts for master (subAccounts)."""
    return _json_text(_info().query_sub_accounts(user))


@mcp.tool()
def hl_user_to_multi_sig_signers(multi_sig_user: str) -> str:
    """Multi-sig signers for address (userToMultiSigSigners)."""
    return _json_text(_info().query_user_to_multi_sig_signers(multi_sig_user))


@mcp.tool()
def hl_perp_deploy_auction_status() -> str:
    """Perp deploy auction status (perpDeployAuctionStatus)."""
    return _json_text(_info().query_perp_deploy_auction_status())


@mcp.tool()
def hl_user_dex_abstraction(user: str) -> str:
    """HIP-3 dex abstraction state (userDexAbstraction)."""
    return _json_text(_info().query_user_dex_abstraction_state(user))


@mcp.tool()
def hl_user_abstraction(user: str) -> str:
    """Unified account / portfolio margin abstraction (userAbstraction)."""
    return _json_text(_info().query_user_abstraction_state(user))


@mcp.tool()
def hl_user_twap_slice_fills(user: str) -> str:
    """Recent TWAP slice fills (userTwapSliceFills)."""
    return _json_text(_info().user_twap_slice_fills(user))


@mcp.tool()
def hl_user_rate_limit(user: str) -> str:
    """User API rate limit info (userRateLimit)."""
    return _json_text(_info().user_rate_limit(user))


@mcp.tool()
def hl_spot_deploy_auction_status(user: str) -> str:
    """Spot deploy auction status for user (spotDeployState)."""
    return _json_text(_info().query_spot_deploy_auction_status(user))


@mcp.tool()
def hl_extra_agents(user: str) -> str:
    """Extra API agents linked to user (extraAgents)."""
    return _json_text(_info().extra_agents(user))


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
