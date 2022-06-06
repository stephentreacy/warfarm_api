import time
from typing import Dict, List

import requests
from flask import Flask, jsonify, request


def get_json(url: str) -> Dict:
    """Returns JSON from URL.

    Parameters
    ----------
    url : str
        URL of the website to retrieve.

    Returns
    -------
    Dict
        JSON returned from the URL.
    """

    try:
        response = requests.get(url, verify=False)
        json = response.json()
    except Exception as e:
        json = {}

    return json


def all_item_ids() -> Dict[int, str]:
    """Returns a dictionary for every item id and name.

    Returns
    -------
    Dict[int, str]
        Tenno Zone ID and item name.
    """

    items = {}
    url = "https://tenno.zone/data"

    items_data = get_json(url)["parts"]
    if not items_data:
        return {}

    for item in items_data:
        if any(
            item["name"].find(part) > -1
            for part in ["Neuroptics", "Chassis", "Systems"]
        ):
            item["name"] = item["name"].replace(" Blueprint", "")

        items[item["id"]] = item["name"]

    return items


def get_items(url_id: str) -> List[str]:
    """Returns the list of item names from a personal tenno.zone link.

    Parameters
    ----------
    url_id : str
        Personal ID string for tenno.zone URL.

    Returns
    -------
    List[str]
        Item names.
    """

    url = "https://tenno.zone/partlist/" + url_id

    items = get_json(url)
    all_items = all_item_ids()

    return [all_items[item] for item in items]


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
    items = get_items(request.values["link"])

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

                buy_orders = sorted(buy_orders)[:5] if buy_orders else buy_orders
                sell_orders = sorted(sell_orders)[:5] if sell_orders else sell_orders

            # Wait between items to keep within 3 API requests per second
            time.sleep(0.35)

        item_orders[item] = {"buy_orders": buy_orders, "sell_orders": sell_orders}

    return jsonify({"data": item_orders})


if __name__ == "__main__":
    app.run()
