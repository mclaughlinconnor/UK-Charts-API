from utils import requests_retry_session
import models
from typing import Union, Dict


class Endpoints:
    @staticmethod
    def track(track_id: str) -> str:
        return f"https://api.deezer.com/track/{track_id}"

    @staticmethod
    def contributor(contributor_id: str) -> str:
        return f"https://api.deezer.com/artist/{contributor_id}"

    @staticmethod
    def album(album_id: str) -> str:
        return f"https://api.deezer.com/album/{album_id}"

    @staticmethod
    def search(parameters: Dict[str, Union[str, int]]) -> str:
        end_point = "https://api.deezer.com/search?q="
        for parameter, value in parameters.items():
            end_point += f"{parameter}: {value}"
        return end_point


class Deezer:
    @staticmethod
    def perform_request(end_point: str) -> Dict:
        resp = requests_retry_session().get(end_point)

        return resp.json()

    @staticmethod
    def get_track_data(track_id: str) -> models.Deezer.Track:

        track_data = Deezer.perform_request(Endpoints.track(track_id))

        album_id = track_data["album"]["id"]
        album_data = Deezer.get_album_data(album_id)

        artist_id = track_data["artist"]["id"]
        artist_data = Deezer.get_contibutor_data(artist_id)

        data = track_data
        data["artist"] = artist_data
        data["album"] = album_data

        return models.Deezer.Track(data, net_req=True)

    @staticmethod
    def get_album_data(album_id: str) -> models.Deezer.Album:
        album_data = Deezer.perform_request(Endpoints.album(album_id))

        return models.Deezer.Album(album_data, net_req=True)

    @staticmethod
    def get_contibutor_data(contibutor_id: str) -> models.Deezer.Contributor:
        contributor_data = Deezer.perform_request(Endpoints.contributor(contibutor_id))

        return models.Deezer.Contributor(contributor_data, net_req=True)
