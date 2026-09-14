import requests
from typing import List, Dict, Any
from src.config import POLYMARKET_API_KEY
from src.connectors.base import BaseConnector, NormalizedOrderBook

class PolymarketClient(BaseConnector):
    """REST client for Polymarket implementing the BaseConnector interface."""

    BASE_URL = "https://clob.polymarket.com"

    def __init__(self):
        self.api_key = POLYMARKET_API_KEY
        self.session = requests.Session()

    def get_markets(self, next_cursor: str = "") -> List[Dict[str, Any]]:
        """Fetch open and active prediction markets from Polymarket."""
        endpoint = f"{self.BASE_URL}/markets"
        params = {
            "active": "true",
            "closed": "false",
        }
        if next_cursor:
            params["next_cursor"] = next_cursor

        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    def get_order_book(self, market_id: str) -> NormalizedOrderBook:
        """Fetch and normalize real-time order book depth for a specific market token."""
        if not market_id:
            return NormalizedOrderBook(market_id=market_id, bids=[], asks=[])

        endpoint = f"{self.BASE_URL}/book"
        params = {"token_id": market_id}
        response = self.session.get(endpoint, params=params)

        if response.status_code in (400, 404):
            return NormalizedOrderBook(market_id=market_id, bids=[], asks=[])

        response.raise_for_status()
        raw_book = response.json()

        bids = [
            {"price": float(b["price"]), "size": float(b["size"])}
            for b in raw_book.get("bids", [])
        ]
        asks = [
            {"price": float(a["price"]), "size": float(a["size"])}
            for a in raw_book.get("asks", [])
        ]

        return NormalizedOrderBook(market_id=market_id, bids=bids, asks=asks)

    