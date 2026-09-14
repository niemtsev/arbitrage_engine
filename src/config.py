import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kalshi API Credentials
KALSHI_API_KEY = os.getenv("KALSHI_API_KEY")
KALSHI_PRIVATE_KEY_PATH = os.getenv("KALSHI_PRIVATE_KEY_PATH")

# Polymarket API Credentials
POLYMARKET_API_KEY = os.getenv("POLYMARKET_API_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/arbitrage")