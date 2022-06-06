# warfarm_api

API for a Discord Bot to retrieve prices from [warframe.market](https://warframe.market/). Used to get a quick overview of prices and decide if the item should be bought or farmed in game.

Receives [tenno.zone](https://tenno.zone/planner/) ID and retrieves selected items. Requests are then made for each item to the [warframe.market API](https://warframe.market/api_docs) to get current buy and sell orders for each item.
