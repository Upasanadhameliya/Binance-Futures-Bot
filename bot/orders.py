from binance.enums import (
    ORDER_TYPE_MARKET,
    ORDER_TYPE_LIMIT,
    TIME_IN_FORCE_GTC,
)


class OrderService:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            params = {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
            }

            if order_type == "MARKET":
                params["type"] = ORDER_TYPE_MARKET

            elif order_type == "LIMIT":
                params["type"] = ORDER_TYPE_LIMIT
                params["timeInForce"] = TIME_IN_FORCE_GTC
                params["price"] = price

            response = self.client.create_order(**params)

            return response

        except Exception as e:
            self.logger.error(f"Order failed: {str(e)}")
            raise