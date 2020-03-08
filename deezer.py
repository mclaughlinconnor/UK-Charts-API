from typing import Dict, Union

import requests

from models import deezer
from utils import requests_retry_session


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

    @staticmethod
    def get_user_data() -> str:
        return "deezer.getUserData"


class Deezer:
    def __init__(self, arl: str, track_id: str) -> None:
        self._setup_session()
        self._login_by_arl(arl)
        self._get_tokens()
        self.track_id = track_id
        self.lyrics = Lyrics(track_id, self)

    def _setup_session(self) -> None:
        self.session = requests.Session()
        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/68.0.3440.106 Safari/537.36"
        )
        http_headers = {
            "User-Agent": user_agent,
            "Content-Language": "en-US",
            "Cache-Control": "max-age=0",
            "Accept": "*/*",
            "Accept-Charset": "utf-8,ISO-8859-1;q=0.7,*;q=0.3",
            "Accept-Language": "en-US;q=0.6,en;q=0.4",
            "Connection": "keep-alive",
        }
        self.session.headers.update(http_headers)

    def _login_by_arl(self, arl: str) -> bool:
        cookies = {"arl": arl}
        self.session.cookies.update(cookies)
        req = self._perform_hidden_request(Endpoints.get_user_data())
        if req["USER"]["USER_ID"]:
            return True
        else:
            return False

    def _perform_hidden_request(self, method: str, json_req: dict = {}) -> dict:
        """ Requests info from the hidden api: gw-light.php.
            Used for loginUserToken(), getCSRFToken()
            and privateApi().
        """
        api_token = "null" if method == Endpoints.get_user_data() else self.csrf_token
        unofficial_api_queries = {
            "api_version": "1.0",
            "api_token": api_token,
            "input": "3",
            "method": method,
        }
        req = (
            requests_retry_session(session=self.session)
            .post(url="https://www.deezer.com/ajax/gw-light.php", params=unofficial_api_queries, json=json_req,)
            .json()
        )
        return req["results"]

    def _get_tokens(self) -> None:
        req = self._perform_hidden_request(Endpoints.get_user_data())
        self.csrf_token = req["checkForm"]
        self.sid_token = req["SESSION_ID"]

    def _perform_request(self, end_point: str) -> Dict:
        resp = requests_retry_session().get(end_point)

        return resp.json()

    def get_track_data(self) -> deezer.Track:

        track_data = self._perform_request(Endpoints.track(self.track_id))

        self.album_id = track_data["album"]["id"]
        album_data = self.get_album_data()

        self.artist_id = track_data["artist"]["id"]
        artist_data = self.get_contibutor_data(self.artist_id)

        data = track_data
        data["artist"] = artist_data
        data["album"] = album_data

        return deezer.Track(data, net_req=True)

    def get_album_data(self) -> deezer.Album:
        album_data = self._perform_request(Endpoints.album(self.album_id))

        return deezer.Album(album_data, net_req=True)

    def get_contibutor_data(self, contibutor_id: str) -> deezer.Contributor:
        contributor_data = self._perform_request(Endpoints.contributor(contibutor_id))

        return deezer.Contributor(contributor_data, net_req=True)

    def get_lyrics(self, synced: bool = False) -> list:
        if synced:
            return self.lyrics.synced_lyrics()
        else:
            return self.lyrics.unsynced_lyrics()


class Lyrics:
    def __init__(self, track_id: str, deezer: Deezer):
        self.track_id = track_id
        self.deezer = deezer
        self._lyric_data: dict = {}

    def _lyrics_request(self) -> dict:
        self._lyric_data = self.deezer._perform_hidden_request("song.getLyrics", {"sng_id": self.track_id})

        return self._lyric_data

    def unsynced_lyrics(self) -> list:
        """ Recieves (timestamped) lyrics from the unofficial api
            and converts them to a conventional .lrc file.
            If only the unsynced lyrics are found, these are written
            to a .txt file.
        """
        if self._lyric_data == {}:
            data = self._lyrics_request()
        else:
            data = self._lyric_data
        if "LYRICS_TEXT" in data:  # unsynced lyrics
            lyrics = data["LYRICS_TEXT"].splitlines()  # True keeps the \n
            return lyrics
        else:
            return []

    def synced_lyrics(self) -> list:
        """ Recieves (timestamped) lyrics from the unofficial api
            and converts them to a conventional .lrc file.
            If only the unsynced lyrics are found, these are written
            to a .txt file.
        """
        if self._lyric_data == {}:
            data = self._lyrics_request()
        else:
            data = self._lyric_data
        if "LYRICS_SYNC_JSON" in data:  # synced lyrics
            lyrics = data["LYRICS_SYNC_JSON"]
            return lyrics
        else:
            return []
