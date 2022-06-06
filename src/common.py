from typing import Dict

import requests


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
