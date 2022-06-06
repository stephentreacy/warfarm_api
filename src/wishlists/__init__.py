from src.wishlists.tenno_zone_wishlist import TennoZoneWishlist
from src.wishlists.xuerian_wishlist import XuerianWishlist


class WishlistFactory:
    def get_wishlist(self, site: str):
        if site == "tennozone":
            return TennoZoneWishlist()
        elif site == "xuerian":
            return XuerianWishlist()
        else:
            raise ValueError(site)
