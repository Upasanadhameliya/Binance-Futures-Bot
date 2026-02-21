import os
from dotenv import load_dotenv
from binance.client import Client

load_dotenv()


class BinanceFuturesClient:
    def __init__(self, logger):
        self.logger = logger

        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("API credentials not found in environment variables")

        self.client = Client(api_key, api_secret)

        # Futures Testnet URL
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def create_order(self, **kwargs):
        self.logger.info(f"Sending order request: {kwargs}")
        response = self.client.futures_create_order(**kwargs)
        self.logger.info(f"Received response: {response}")
        return response