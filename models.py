import datetime
from typing import Dict, Any


class Deezer:
    class Track:
        def __init__(self, data: Dict[str, Any]) -> None:
            self.deezer_id: str = data["deezer_id"]
            self.title: str = data["title"]
            self.title_short: str = data["title_short"]
            self.title_version: str = data["title_version"]
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
            self.contributors: Deezer.Contributor = data["contributors"]
            self.artist: Deezer.Contributor = data["artist"]
            self.album: str = data["album"]

    class Contributor:
        def __init__(self, data: Dict[str, Any]):
            self.id: int = data["id"]
            self.name: str = data["name"]
            self.link: str = data["link"]
            self.picture: Deezer.Picture = data["picture"]
            self.radio: bool = data["radio"]
            self.track_list: str = data["track_list"]
            self.type: str = data["type"]

    class Picture:
        def __init__(self, data: Dict[str, Any]):
            self.thumbnail: str = data["thumbnail"]
            self.small: str = data["small"]
            self.medium: str = data["medium"]
            self.big: str = data["big"]
            self.xl: str = data["xl"]

    class Album:
        def __init__(self, data: Dict[str, Any]):
            self.id: int = data["id"]
            self.title: str = data["title"]
            self.link: str = data["link"]
            self.cover: Deezer.Picture = data["cover"]
            self.release_date: datetime.date = data["release_date"]
            self.track_list: str = data["track_list"]
