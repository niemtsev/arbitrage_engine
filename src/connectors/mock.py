from typing import List, Dict, Any
from src.connectors.base import BaseConnector, NormalizedOrderBook

class MockClient(BaseConnector):
    """Mock prediction market connector for local testing and spread calculations."""

    def __init__(self, mock_bids: List[Dict[str, float]] = None, mock_asks: List[Dict[str, float]] = None):
        self.mock_bids = mock_bids or [{"price": 0.48, "size": 100.0}]
        self.mock_asks = mock_asks or [{"price": 0.51, "size": 150.0}]

    def get_markets(self) -> List[Dict[str, Any]]:
        """Return simulated market listing."""
        return [{"id": "mock_election_2026", "question": "Will candidate X win?"}]

    def get_order_book(self, market_id: str) -> NormalizedOrderBook:
        """Return deterministic order book depth for spread validation."""
        return NormalizedOrderBook(
            market_id=market_id,
            bids=self.mock_bids,
            asks=self.mock_asks
        )