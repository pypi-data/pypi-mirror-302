"""Top trading pair queries.

- Data structures for /top end point

- Used for adding new pairs to open ended trading universe in external trading signal processor

- See :py:func:`tradingstrategy.client.Client.fetch_top_pairs` for usage.
"""
import datetime

from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, config
from marshmallow import fields


@dataclass_json
@dataclass(slots=True)
class TopPairData:
    """See open-defi-api.yaml"""

    #: When this entry was queried
    #:
    #: Wall clock UTC time.
    #:
    #: Because the server serialises as ISO, we need special decoder
    #:
    #: https://github.com/lidatong/dataclasses-json?tab=readme-ov-file#Overriding
    #:
    queried_at: datetime.datetime = field(
        metadata=config(
            decoder=datetime.datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )

    #: Blockchain this pair is on
    chain_id: int

    #: Internal pair primary key (may change)
    pair_id: int

    #: Internal pair exchange id (may change)
    exchange_id: int

    #: Human readable exchange URL slug (may change)
    exchange_slug: str

    #: Smart contract address of pool smart contract.
    #:
    #: Uniswap v2 pair contract address, Uniswap v3 pool contract address.
    #:
    pool_address: str

    #: Human readable base token
    base_token: str

    #: Human readable quote token
    quote_token: str

    #: Pair fee in 0...1, 0.0030 is 30 BPS
    fee: float

    #: Volume over the last 24h
    #:
    #: May not be available due to latency/denormalisation/etc. issues
    #:
    volume_24h_usd: float | None

    #: Last USD TVL (Uniswap v3) or XY Liquidity (Uniswap v2)
    #:
    #: May not be available due to latency/denormalisation/etc. issues
    #:
    tvl_latest_usd: float | None

    #: When TVL measurement was updated.
    #:
    #: How old data are we using.
    #:
    tvl_updated_at: datetime.datetime | None = field(
        metadata=config(
            decoder=datetime.datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


    #: When volume measurement was updated
    #:
    #: How old data are we using.
    #:
    volume_updated_at: datetime.datetime | None = field(
        metadata=config(
            decoder=datetime.datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


    #: If this pair was excluded from the top pairs, what was the human-readable heuristics reason we did this.
    #:
    #: This allows you to diagnose better why some trading pairs might not end up in the trading universe.
    #:
    exclude_reason: str | None

    #: TokenSniffer data for this token.
    #:
    #: Used in the filtering of scam tokens.
    #:
    #: Not available for all tokens that are filtered out for other reasons.
    #: This is the last check.
    #:
    #: `See more information here <https://web3-ethereum-defi.readthedocs.io/api/token_analysis/_autosummary_token_analysis/eth_defi.token_analysis.tokensniffer.html>`__.
    #:
    token_sniffer_data: dict | None

    def __repr__(self):
        return f"<Pair {self.base_token} - {self.quote_token} on {self.exchange_slug}, address {self.pool_address} - reason {self.exclude_reason}>"

    def get_ticker(self) -> str:
        """Simple marker ticker identifier for this pair."""
        return f"{self.base_token} - {self.quote_token}"

    def get_persistent_string_id(self) -> str:
        """Stable id over long period of time and across different systems."""
        return f"{self.chain_id}-{self.pool_address}"

    @property
    def token_sniffer_score(self) -> int | None:
        """What was the TokenSniffer score for the base token."""

        if self.token_sniffer_data is None:
            return None

        return self.token_sniffer_data["score"]


@dataclass_json
@dataclass(slots=True)
class TopPairsReply:
    """/top endpoint reply.

    - Get a list of trading pairs, both included and excluded

    """

    #: The top list at the point of time the request was made
    included: list[TopPairData]

    #: Tokens that were considered for top list, but excluded for some reason
    #:
    #: They had enough liquidity, but they failed e.g. TokenSniffer scam check,
    #: or had a trading pair for the same base token with better fees, etc.
    #:
    excluded: list[TopPairData]