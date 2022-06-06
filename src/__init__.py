import time
from typing import Dict, List

from flask import Flask, jsonify, request

from src.common import get_json
from src.wishlists import WishlistFactory


def get_market_prices(item: str) -> List[Dict]:
    """Gets the orders of an item.

    Parameters
    ----------
    item : str
        Name of item.

    Returns
    -------
    List[Dict]
        All orders for the item.
    """

    api_url = "https://api.warframe.market/v1/items/"
    name_url = (
        item.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("'", "")
        .replace("&", "and")
    )
    url_item = api_url + name_url + "/orders"

    item_json = get_json(url_item)

    return item_json["payload"]["orders"]


app = Flask(__name__)


@app.route("/check")
def check():
    return jsonify({"hello": "world"})


@app.route("/orders")
def orders_json():
    website = request.values["site"]
    token = request.values["token"]

    wishlist = WishlistFactory().get_wishlist(website)
    items = wishlist.get_wishlist_items(token)

    item_orders = {}

    for item in items:
        orders = get_market_prices(item)

        if orders:
            buy_orders = []
            sell_orders = []

            for order in orders:
                if order["user"]["status"] == "ingame" and order["order_type"] == "buy":
                    buy_orders.append(order["platinum"])
                elif (
                    order["user"]["status"] == "ingame"
                    and order["order_type"] == "sell"
                ):
                    sell_orders.append(order["platinum"])

                buy_orders = sorted(buy_orders)[-5:] if buy_orders else buy_orders
                sell_orders = sorted(sell_orders)[:5] if sell_orders else sell_orders

            # Wait between items to keep within 3 API requests per second
            time.sleep(0.35)

        item_orders[item] = {"buy_orders": buy_orders, "sell_orders": sell_orders}

    return jsonify({"data": item_orders})


if __name__ == "__main__":
    app.run()
