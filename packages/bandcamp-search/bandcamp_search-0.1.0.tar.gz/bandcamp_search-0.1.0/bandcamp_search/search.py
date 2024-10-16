import requests

from bandcamp_search.models import BandcampResponse, SearchType


def search(query: str, search_filter: SearchType) -> BandcampResponse:
    data = {
        "search_filter": search_filter.value,
        "search_text": query,
        "fan_id": None,
        "full_page": False,
    }

    response = requests.post(
        "https://bandcamp.com/api/bcsearch_public_api/1/autocomplete_elastic",
        json=data,
    )
    response.raise_for_status()

    return response.json()
