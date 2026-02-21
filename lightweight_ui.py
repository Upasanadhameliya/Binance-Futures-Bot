import tkinter as tk
from tkinter import ttk, messagebox
import traceback

from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logger


class OrderUI:
    def __init__(self, root):
        self.logger = setup_logger()
        self.client = BinanceFuturesClient(self.logger)
        self.service = OrderService(self.client, self.logger)

        self.root = root
        root.title("Binance Futures - Lightweight UI")

        frm = ttk.Frame(root, padding=12)
        frm.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Symbol
        ttk.Label(frm, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        ttk.Entry(frm, textvariable=self.symbol_var, width=20).grid(row=0, column=1)

        # Side
        ttk.Label(frm, text="Side:").grid(row=1, column=0, sticky=tk.W)
        self.side_var = tk.StringVar(value="BUY")
        side_menu = ttk.Combobox(frm, textvariable=self.side_var, values=["BUY", "SELL"], state="readonly", width=17)
        side_menu.grid(row=1, column=1)

        # Type
        ttk.Label(frm, text="Type:").grid(row=2, column=0, sticky=tk.W)
        self.type_var = tk.StringVar(value="MARKET")
        type_menu = ttk.Combobox(frm, textvariable=self.type_var, values=["MARKET", "LIMIT"], state="readonly", width=17)
        type_menu.grid(row=2, column=1)
        type_menu.bind("<<ComboboxSelected>>", self.on_type_change)

        # Quantity
        ttk.Label(frm, text="Quantity:").grid(row=3, column=0, sticky=tk.W)
        self.qty_var = tk.StringVar(value="0.001")
        ttk.Entry(frm, textvariable=self.qty_var, width=20).grid(row=3, column=1)

        # Price
        ttk.Label(frm, text="Price (for LIMIT):").grid(row=4, column=0, sticky=tk.W)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(frm, textvariable=self.price_var, width=20)
        self.price_entry.grid(row=4, column=1)

        # Buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        place_btn = ttk.Button(btn_frame, text="Place Order", command=self.place_order)
        place_btn.grid(row=0, column=0, padx=6)

        quit_btn = ttk.Button(btn_frame, text="Quit", command=root.quit)
        quit_btn.grid(row=0, column=1, padx=6)

        # Status
        self.status = tk.StringVar(value="Ready")
        ttk.Label(frm, textvariable=self.status).grid(row=6, column=0, columnspan=2, pady=(8, 0))

        # Initialize state
        self.on_type_change()

    def on_type_change(self, event=None):
        order_type = self.type_var.get()
        if order_type == "MARKET":
            self.price_entry.state(["disabled"])
            self.price_var.set("")
        else:
            try:
                self.price_entry.state(["!disabled"])
            except Exception:
                pass

    def place_order(self):
        symbol = self.symbol_var.get().strip()
        side = self.side_var.get().strip()
        order_type = self.type_var.get().strip()
        qty_str = self.qty_var.get().strip()
        price_str = self.price_var.get().strip() or None

        try:
            # Convert quantity and price
            quantity = float(qty_str)
            price = float(price_str) if price_str is not None and price_str != "" else None

            # Validation
            validate_side(side)
            validate_order_type(order_type)
            validate_quantity(quantity)
            validate_price(order_type, price)

            # Update status
            self.status.set("Placing order...")
            self.root.update_idletasks()

            response = self.service.place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )

            order_id = response.get("orderId")
            status = response.get("status")
            executed = response.get("executedQty")
            avg_price = response.get("avgPrice", "N/A")

            msg = f"Order placed successfully.\nOrder ID: {order_id}\nStatus: {status}\nExecuted Qty: {executed}\nAvg Price: {avg_price}"
            messagebox.showinfo("Order Success", msg)
            self.status.set("Order success")

        except Exception as e:
            tb = traceback.format_exc()
            self.logger.error(f"Order failed: {e}\n{tb}")
            messagebox.showerror("Order Failed", str(e))
            self.status.set("Order failed")


def main():
    root = tk.Tk()
    app = OrderUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
