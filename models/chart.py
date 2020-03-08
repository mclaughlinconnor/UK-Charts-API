from typing import Any, Dict, Optional

from deezer import Deezer
from utils import read_arl


class ChartData:
    def __init__(self, data: Dict[str, Any]):
        self.title = data["title"]
        self.artist = data["artist"]
        self.position = data["position"]
        self.last_week = data["last_week"]
        self.label = data["label"]
        self.peak = data["peak"]
        self.woc = data["woc"]

    def set_stream_urls(self, deezer_id: str, spotify_id: str) -> None:
        if deezer_id is not None:
            self.deezer_id: str = deezer_id
        if spotify_id is not None:
            self.spotify_id: str = spotify_id

    def to_deezer(self) -> Optional[Deezer]:
        try:
            return Deezer(read_arl("arl.txt"), self.deezer_id)
        except NameError:
            raise ValueError(f"No deezer id for song {self.title} by {self.artist}")
