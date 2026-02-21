import argparse
import sys

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logger


def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet CLI")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    logger = setup_logger()

    try:
        # Validation
        validate_side(args.side)
        validate_order_type(args.type)
        validate_quantity(args.quantity)
        validate_price(args.type, args.price)

        # Setup client & service
        client = BinanceFuturesClient(logger)
        order_service = OrderService(client, logger)

        print("\n===== ORDER REQUEST =====")
        print(f"Symbol   : {args.symbol}")
        print(f"Side     : {args.side}")
        print(f"Type     : {args.type}")
        print(f"Quantity : {args.quantity}")
        print(f"Price    : {args.price}")
        print("=========================\n")

        response = order_service.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        print("✅ ORDER SUCCESS")
        print(f"Order ID     : {response.get('orderId')}")
        print(f"Status       : {response.get('status')}")
        print(f"Executed Qty : {response.get('executedQty')}")
        print(f"Avg Price    : {response.get('avgPrice', 'N/A')}")

    except Exception as e:
        print("❌ ORDER FAILED")
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()