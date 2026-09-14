from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class NormalizedOrderBook:
    market_id: str
    bids: List[Dict[str, float]]  # Standardized: [{'price': float, 'size': float}]
    asks: List[Dict[str, float]]  # Standardized: [{'price': float, 'size': float}]

class BaseConnector(ABC):
    """Abstract base class establishing the contract for all prediction market connectors."""

    @abstractmethod
    def get_markets(self) -> List[Dict[str, Any]]:
        """Fetch active prediction markets from the exchange."""
        pass

    @abstractmethod
    def get_order_book(self, market_id: str) -> NormalizedOrderBook:
        """Fetch and normalize real-time order book depth for a specific market."""
        pass

    