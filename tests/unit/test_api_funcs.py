from unittest import TestCase, mock

from src import all_item_ids, get_items, get_json, get_market_prices


class TestAPIFunctions(TestCase):
    def setUp(self):
        self.expected_json = {
            "parts": [
                {"id": 1, "setId": 1, "name": "Akbolto Prime Barrel", "ducats": 45},
                {"id": 2, "setId": 1, "name": "Akbolto Prime Blueprint", "ducats": 15},
                {"id": 3, "setId": 1, "name": "Akbolto Prime Link", "ducats": 45},
                {"id": 4, "setId": 1, "name": "Akbolto Prime Receiver", "ducats": 100},
                {"id": 16, "setId": 6, "name": "Ash Prime Blueprint", "ducats": 45},
                {
                    "id": 17,
                    "setId": 6,
                    "name": "Ash Prime Chassis Blueprint",
                    "ducats": 15,
                },
                {
                    "id": 18,
                    "setId": 6,
                    "name": "Ash Prime Neuroptics Blueprint",
                    "ducats": 45,
                },
                {
                    "id": 19,
                    "setId": 6,
                    "name": "Ash Prime Systems Blueprint",
                    "ducats": 65,
                },
            ]
        }
        self.expected_item_ids = {
            1: "Akbolto Prime Barrel",
            2: "Akbolto Prime Blueprint",
            3: "Akbolto Prime Link",
            4: "Akbolto Prime Receiver",
            16: "Ash Prime Blueprint",
            17: "Ash Prime Chassis",
            18: "Ash Prime Neuroptics",
            19: "Ash Prime Systems",
        }

        self.requests_response = mock.Mock(json=lambda: self.expected_json)

        self.orders = {
            "payload": {
                "orders": [
                    {
                        "order_type": "sell",
                        "quantity": 3,
                        "platinum": 10,
                        "user": {
                            "reputation": 9,
                            "region": "en",
                            "last_seen": "2022-06-02T14:06:08.396+00:00",
                            "ingame_name": "name1",
                            "id": "abcd1234",
                            "avatar": None,
                            "status": "ingame",
                        },
                        "platform": "pc",
                        "region": "en",
                        "creation_date": "2019-01-21T08:40:37.000+00:00",
                        "last_update": "2020-05-25T09:00:32.000+00:00",
                        "visible": True,
                        "id": "1234abcd",
                    },
                    {
                        "quantity": 1,
                        "order_type": "buy",
                        "platinum": 2,
                        "visible": True,
                        "user": {
                            "reputation": 1,
                            "region": "en",
                            "avatar": None,
                            "last_seen": "2022-06-05T16:27:39.729+00:00",
                            "ingame_name": "name2",
                            "id": "efgh5678",
                            "status": "ingame",
                        },
                        "platform": "pc",
                        "region": "en",
                        "creation_date": "2022-05-04T09:26:59.000+00:00",
                        "last_update": "2022-05-08T13:28:41.000+00:00",
                        "id": "5675efgh",
                    },
                ]
            }
        }

    @mock.patch("src.requests.get")
    def test_get_json(self, mock_get):
        mock_get.return_value = self.requests_response

        response_json = get_json("url")

        self.assertEqual(response_json, self.expected_json)

    @mock.patch("src.get_json")
    def test_all_item_ids(self, mock_get_json):
        mock_get_json.return_value = self.expected_json

        item_ids = all_item_ids()

        self.assertEqual(item_ids, self.expected_item_ids)

    @mock.patch("src.get_json")
    @mock.patch("src.all_item_ids")
    def test_get_items(self, mock_all_item_ids, mock_get_json):
        mock_all_item_ids.return_value = self.expected_item_ids
        mock_get_json.return_value = list(self.expected_item_ids.keys())

        items = get_items("abc")

        self.assertEqual(items, list(self.expected_item_ids.values()))

    def test_get_market_prices_converts_name(self):
        pass

    @mock.patch("src.get_json")
    def test_get_market_prices_returns_orders(self, mock_get_json):
        mock_get_json.return_value = self.orders

        orders = get_market_prices(self.expected_item_ids[1])

        self.assertEqual(orders, self.orders["payload"]["orders"])
