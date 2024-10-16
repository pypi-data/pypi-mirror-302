from enum import StrEnum
from typing import Any, TypedDict


class SearchType(StrEnum):
    ALL = ""
    ALBUMS = "a"
    ARTISTS_AND_LABELS = "b"
    TRACKS = "t"


class SearchResult(TypedDict):
    type: SearchType
    id: int
    art_id: int
    img_id: int
    name: str


class ArtistLabelSearchResult(SearchResult):
    item_url_root: str
    location: str
    is_label: bool
    img: str
    tag_names: list[str]
    genre_name: str
    stat_params: str


class TrackSearchResult(SearchResult):
    album_name: str
    album_id: int
    band_id: int
    band_name: str
    item_url_root: str
    item_url_path: str
    img: str
    stat_params: str


class AlbumSearchResult(SearchResult):
    band_id: int
    band_name: str
    item_url_root: str
    item_url_path: str
    img: str
    tag_names: list[str]
    stat_params: str


class AutoCompleteResult(TypedDict):
    results: list[AlbumSearchResult | ArtistLabelSearchResult | TrackSearchResult]
    stat_params_for_tag: str
    time_ms: int


class BandcampResponse(TypedDict):
    auto: AutoCompleteResult
    tag: dict[str, Any]
    genre: dict[str, Any]
