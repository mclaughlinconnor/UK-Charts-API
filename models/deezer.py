import datetime
from typing import Any, Dict, List, Optional

from endpoints import Endpoints
from utils import dict_rename, requests_retry_session


class Track:
    def __init__(
        self, data: Dict[str, Any], spotify_url: str = None, net_req: bool = False, skip_children: bool = False
    ):
        if net_req:
            data = self._net_req_convert(data, skip_children)

        self.deezer_id: str = data["deezer_id"]
        self.title: str = data["title"]
        self.title_short: str = data["title_short"]
        self.isrc: str = data["isrc"]
        self.link: str = data["link"]
        self.duration: int = data["duration"]
        self.track_position: int = data["track_position"]
        self.disk_number: int = data["disk_number"]
        self.rank: int = data["rank"]
        self.release_date: datetime.date = data["release_date"]
        self.explicit_lyrics: bool = data["explicit_lyrics"]
        self.preview_url: str = data["preview_url"]
        self.bpm: int = data["bpm"]
        self.gain: float = data["gain"]
        self.contributors: List[int] = data["contributors"]
        self.artist: Contributor = data["artist"]
        self.album: Album = data["album"]
        self.spotify_url: Optional[str] = spotify_url

        if "title_version" in data:
            self.title_version: str = data["title_version"]

    def _net_req_convert(self, data: Dict[str, Any], skip_children: bool = False) -> Dict[str, Any]:
        rename = {"id": "deezer_id", "preview": "preview_url"}
        remove = [
            "share",
            "explicit_content_lyrics",
            "explicit_content_cover",
            "available_countries",
        ]

        for original, new in rename.items():
            data[new] = data[original]
            data.pop(original)

        for field in remove:
            data.pop(field)

        data["contributors"] = [contrib_data["id"] for contrib_data in data["contributors"]]

        if not skip_children:
            if not isinstance(data["artist"], Contributor):
                data["artist"] = Contributor(data["artist"])
            if not isinstance(data["album"], Album):
                data["album"] = Album(data["album"])

        return data


class Contributor:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.link: str = data["link"]
        self.picture: Picture = data["picture"]
        self.albums: int = data["albums"]
        self.fans: int = data["fans"]
        self.track_list: str = data["track_list"]

    def _net_req_convert(self, data: Dict[str, Any]) -> Dict[str, Any]:
        removed = ["share", "radio", "type"]
        renamed = {"nb_album": "albums", "nb_fan": "fans", "tracklist": "track_list"}

        for field in removed:
            data.pop(field)

        for original, new in renamed.items():
            data[new] = data[original]
            data.pop(original)

        data["picture"] = Picture(data, net_req=True)

        return data


class Picture:
    def __init__(self, data: Dict[str, Any], net_req: bool = False, prefix: str = "picture"):
        if net_req:
            data = self._net_req_convert(data, prefix)

        self.thumbnail: str = data["thumbnail"]
        self.small: str = data["small"]
        self.medium: str = data["medium"]
        self.big: str = data["big"]
        self.xl: str = data["xl"]

    def _net_req_convert(self, data: Dict[str, Any], prefix: str = "picture") -> Dict[str, Any]:
        keys = {
            f"{prefix}": "thumbnail",
            f"{prefix}_small": "small",
            f"{prefix}_medium": "medium",
            f"{prefix}_big": "big",
            f"{prefix}_xl": "xl",
        }

        picture_data = {}
        for original, new in keys.items():
            picture_data[new] = data[original]

        return picture_data

    @property
    def _url_prefix(self) -> str:
        return "/".join(self.xl.split("/")[0:-1])

    def cover_art(self, size: int) -> bytes:
        """ Retrieves the cover art/playlist image from the official API,
            downloads and returns it.
        """
        url = f"{self._url_prefix}/{size}x{size}.png"
        r = requests_retry_session().get(url)
        return r.content


class Album:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)

        self.id: int = data["id"]
        self.title: str = data["title"]
        self.upc: str = data["upc"]
        self.link: str = data["link"]
        self.cover: Picture = data["cover"]
        self.genres: List[Genre] = data["genres"]
        self.label: str = data["label"]
        self.duration: int = data["duration"]
        self.fans: int = data["fans"]
        self.rating: int = data["rating"]
        self.release_date: datetime.date = data["release_date"]
        self.record_type = data["record_type"]
        self.track_list: str = data["track_list"]
        self.explicit_lyrics: bool = data["explicit_lyrics"]
        self.explicit_content_lyrics: bool = data["explicit_content_lyrics"]
        self.explicit_content_cover: bool = data["explicit_content_cover"]
        self.contributors: List[int] = data["contributors"]
        self.artist: Contributor = data["artist"]
        self.track_count: int = data["track_count"]

    @property
    def id3v24_release_date(self) -> str:
        return self.release_date.strftime("%Y%m%d")

    @property
    def genre_list(self) -> List[str]:
        genres = [genre.name for genre in self.genres]
        return genres

    def _net_req_convert(self, data: Dict[str, Any]) -> Dict[str, Any]:

        rename = {"tracklist": "track_list", "nb_tracks": "track_count"}
        cover_keys = ["cover", "cover_small", "cover_medium", "cover_big", "cover_xl"]

        data["contributors"] = [contrib_data["id"] for contrib_data in data["contributors"]]
        data["genres"] = [Genre(genre_data, net_req=True) for genre_data in data["genres"]["data"]]
        data["release_date"] = datetime.datetime.strptime(data["release_date"], "%Y-%m-%d")
        data["artist"] = Contributor(data["artist"], net_req=True)

        cover_data = {}
        for key in cover_keys:
            cover_data[key] = data[key]

        data["cover"] = Picture(cover_data, net_req=True, prefix="cover")

        data = dict_rename(data, rename)

        # Means that a Track() doesn't reference an Album() that contains the same Track()
        data.pop("tracks")

        return data


class Genre:
    def __init__(self, data: Dict[str, Any], net_req: bool = False):
        if net_req:
            data = self._net_req_convert(data)

        self.id: int = data["id"]
        self.name: str = data["name"]
        self.picture: Picture = data["picture"]

    def _net_req_convert(self, data: dict) -> dict:
        genre_data = self._perform_request(Endpoints.genre(str(data["id"])))
        genre_data = cast(dict, genre_data)

        data["picture"] = Picture(genre_data, net_req=True, prefix="picture")

        return data
