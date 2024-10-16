# bandcamp-search

Library to search for music on Bandcamp.


## Installation
```bash
pip install bandcamp-search
```

## Usage
Sample usage is in `bandcamp_search/__main__.py`:

```python
import sys
from typing import cast

from bandcamp_search.search import search
from bandcamp_search.models import (
    AlbumSearchResult,
    ArtistLabelSearchResult,
    SearchType,
    TrackSearchResult,
)

if __name__ == "__main__":
    query = sys.argv[1]
    results = search(query, SearchType.ALL)
    for result in results["auto"]["results"]:
        if result["type"] == SearchType.ALBUMS:
            result = cast(AlbumSearchResult, result)
            print(f"Album: {result['name']}")
            print(f"  by {result['band_name']}")
            print(f"  buy at {result['item_url_path']}")
        if result["type"] == SearchType.ARTISTS_AND_LABELS:
            result = cast(ArtistLabelSearchResult, result)
            print("Artist/Label: {result['name']}")
            print(f"  {result['location']}")
        if result["type"] == SearchType.TRACKS:
            result = cast(TrackSearchResult, result)
            print(f"Track: {result['name']}")
            print(f"  on {result['album_name']} by {result['band_name']}")
            print(f"  listen at {result['item_url_path']}")
```
