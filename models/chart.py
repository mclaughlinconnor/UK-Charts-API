from typing import Any, Dict, Optional

from deezer import Deezer
from utils import read_arl, url_to_deezer_id


class ChartSong:
    def __init__(self, data: Dict[str, Any]):
        self.title = data["title"]
        self.artist = data["artist"]
        self.label = data["label"]
        self.woc = data["woc"]
        self.peak = data["peak"]

    def set_stream_urls(self, deezer_id: str, spotify_id: str) -> None:
        if deezer_id is not None:
            self.deezer_id: str = deezer_id
        if spotify_id is not None:
            self.spotify_id: str = spotify_id

    def to_deezer(self) -> Optional[Deezer]:
        try:
            return Deezer(read_arl("arl.txt"), url_to_deezer_id(self.deezer_id))
        except NameError:
            raise ValueError(f"No deezer id for song {self.title} by {self.artist}")



class ChartData:
    def __init__(self, data: Dict[str, Any]):
        self.chart_id = data["chart_id"]
        self.chart_title = data["chart_title"]
        self.chart_song = data["chart_song"]
        self.position = data["position"]
        self.date = data["date"]
        self.chart_url = data["chart_url"]
        self.last_week = data["last_week"]
