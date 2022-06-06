from typing import Dict, List

from src.common import get_json


class TennoZoneWishlist:
    def get_wishlist_items(self, token: str) -> List[str]:
        """Returns the list of item names from a personal tenno.zone link.

        Parameters
        ----------
        token : str
            Unique token of user.

        Returns
        -------
        List[str]
            Item names.
        """

        wishlist_url = "https://tenno.zone/partlist/" + token

        items = get_json(wishlist_url)
        all_items = _all_item_ids()

        return [all_items[item] for item in items]


def _all_item_ids() -> Dict[int, str]:
    """Returns a dictionary for every item id and name.

    Returns
    -------
    Dict[int, str]
        Tenno Zone ID and item name.
    """

    items = {}

    items_data = get_json("https://tenno.zone/data")["parts"]
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
