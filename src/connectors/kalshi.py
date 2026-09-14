import requests
from src.config import KALSHI_API_KEY, KALSHI_PRIVATE_KEY_PATH

class KalshiClient:
    """REST client for interacting with the Kalshi API."""

    BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

    def __init__(self):
        self.api_key = KALSHI_API_KEY
        self.private_key_path = KALSHI_PRIVATE_KEY_PATH
        self.session = requests.Session()

    def get_exchange_status(self) -> dict:
        """Fetch current Kalshi exchange status."""
        endpoint = f"{self.BASE_URL}/exchange/status"
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json()
    