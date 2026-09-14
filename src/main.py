import sys
from pathlib import Path

# Insert project root directory into sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.connectors.polymarket import PolymarketClient
from src.connectors.mock import MockClient
from src.engine.detector import ArbitrageDetector

def run_scanner():
    print("=== Prediction Market Arbitrage Engine ===")
    
    poly_client = PolymarketClient()
    mock_client = MockClient(mock_asks=[{"price": 0.47, "size": 100.0}])

    markets = poly_client.get_markets()
    print(f"[*] Loaded {len(markets)} active Polymarket markets.")

    opportunities = 0

    # Scan top active market tokens against simulated secondary venue
    for market in markets[:10]:
        question = market.get("question", "Unknown Question")
        tokens = market.get("tokens", [])

        for token in tokens:
            token_id = token.get("token_id")
            if not token_id:
                continue

            poly_book = poly_client.get_order_book(token_id)
            mock_book = mock_client.get_order_book(token_id)

            arb = ArbitrageDetector.check_complement_arbitrage(poly_book, mock_book)
            if arb:
                opportunities += 1
                print(f"\n[!] OPPORTUNITY FOUND: {question}")
                print(f"    Polymarket Ask: ${arb['venue_a_ask']}")
                print(f"    Mock Venue Ask: ${arb['venue_b_ask']}")
                print(f"    Total Risk Cost: ${arb['total_cost']} | Expected Profit: {arb['profit_margin'] * 100:.2f}%")

    print(f"\n[*] Scan complete. Total opportunities identified: {opportunities}")

if __name__ == "__main__":
    run_scanner()
