from typing import List

import requests


class XuerianWishlist:
    def get_wishlist_items(self, token: str) -> List[str]:
        """Returns the list of item names from a personal xuerian link.

        Parameters
        ----------
        token : str
            Unique token of user.

        Returns
        -------
        List[str]
            Item names.
        """
        self.wishlist_url = "https://wf.xuerian.net/api/load"

        response = requests.post(self.wishlist_url, {"tokens": token})

        items = response.json()[token]["wants"]

        for idx, item in enumerate(items):
            if any(
                item.find(part) > -1 for part in ["Neuroptics", "Chassis", "Systems"]
            ):
                items[idx] = item.replace(" Blueprint", "")

        return items
