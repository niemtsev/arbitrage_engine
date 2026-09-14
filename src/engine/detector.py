from typing import Dict, Optional
from src.connectors.base import NormalizedOrderBook

class ArbitrageDetector:
    """Calculates cross-venue and complementary arbitrage opportunities across normalized order books."""

    @staticmethod
    def check_complement_arbitrage(
        book_a: NormalizedOrderBook, 
        book_b: NormalizedOrderBook, 
        min_margin: float = 0.01
    ) -> Optional[Dict[str, float]]:
        """
        Checks if buying YES on Venue A and NO on Venue B guarantees a profit payout of $1.00.
        """
        if not book_a.asks or not book_b.asks:
            return None

        best_ask_a = min(ask["price"] for ask in book_a.asks)
        best_ask_b = min(ask["price"] for ask in book_b.asks)

        total_cost = best_ask_a + best_ask_b
        profit_margin = 1.00 - total_cost

        if profit_margin >= min_margin:
            return {
                "venue_a_ask": best_ask_a,
                "venue_b_ask": best_ask_b,
                "total_cost": round(total_cost, 4),
                "profit_margin": round(profit_margin, 4)
            }
        
        return None