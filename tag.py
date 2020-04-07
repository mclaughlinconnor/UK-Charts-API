import acoustid
from deezer import Deezer
from utils import sort_title
from mutagen.id3 import (
    APIC,
    RVA2,
    TALB,
    TBPM,
    TCON,
    TDEN,
    TDRL,
    TIT2,
    TPE1,
    TPE2,
    TPOS,
    TPUB,
    TRCK,
    TRSN,
    TSOA,
    TSOP,
    TSOT,
    TSRC,
    TXXX,
    USLT,
    WXXX,
)
from mutagen.mp3 import MP3
import time
from typing import Any
from mb import Musicbrainz


class Tag:
    @staticmethod
    def add_tag(f: MP3, tag: Any) -> None:
        try:
            f.tags.add(f, tag)
        except ValueError:
            return

    def _calculate_acoustid_fingerprint(self, filename: str) -> list:
        duration, fingerprint = acoustid.fingerprint_file(filename)

        return [duration, fingerprint]

    @staticmethod
    def _tag_mp3(self, filename: str, deezer: Deezer) -> None:
        filename = f"{filename}.mp3"
        f = MP3()

        f.add_tags()

        duration, acoustid_fingerprint = self._calculate_acoustid_fingerprint(filename)
        mb_ids = self._mb_id(deezer.artist_id, deezer.track.title)

        self.add_tag(f, TPUB(encoding=3, text=deezer.album.label))
        self.add_tag(f, TSOT(encoding=3, text=deezer.track.title))
        self.add_tag(f, TSOA(encoding=3, text=sort_title(deezer.album.title)))
        self.add_tag(f, TSOP(encoding=3, text=deezer.contributor.name))
        self.add_tag(f, TDEN(text=time.strftime("%d/%m/%Y %H:%M:%S")))
        self.add_tag(f, TIT2(encoding=3, text=deezer.track.title))
        self.add_tag(f, TPOS(text=deezer.track.disk_number))
        self.add_tag(f, TRCK(text=deezer.track.track_position))
        self.add_tag(f, TDRL(text=deezer.album.release_date))
        self.add_tag(f, TPE1(text=deezer.album.contributors))
        self.add_tag(f, TPE2(text=deezer.contributor.name))
        self.add_tag(f, TBPM(text=deezer.track.bpm))
        self.add_tag(f, RVA2(desc="", channel=1, gain=deezer.track.gain))
        self.add_tag(f, USLT(text=deezer.lyrics.unsynced_lyrics()))
        self.add_tag(f, TCON(text=deezer.album.genres))
        self.add_tag(f, TXXX(text=deezer.album.upc, desc="upc"))
        self.add_tag(f, TALB(text=deezer.album.title))
        self.add_tag(f, WXXX(url=deezer.album.link, desc="album_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.track.link, desc="song_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.contributor.link, desc="artist_deezer_url"))
        self.add_tag(f, WXXX(url=deezer.track.spotify_url, desc="song_spotify_id"))
        self.add_tag(f, WXXX(url=acoustid_fingerprint, desc="acoust_id_fingerprint"))
        self.add_tag(
            f, APIC(type=3, data=deezer.album.cover.cover_art(1500), mime="image/jpeg")
        )  # 8 is artist, 3 is album
        self.add_tag(
            f, APIC(type=3, data=deezer.contributor.picture.cover_art(1500), mime="image/jpeg")
        )  # 8 is artist, 3 is album
        self.add_tag(f, TSRC(text=deezer.track.isrc))
        self.add_tag(f, TRSN(text="Deezer"))

        if mb_ids is not None:
            self.add_tag(f, TXXX(text=mb_ids["artist"], desc="musicbrainz_albumartistid"))
            self.add_tag(f, TXXX(text=mb_ids["album"], desc="musicbrainz_albumid"))

        f.save(filename)

    def _mb_id(self, artist, title, acid_fps):
        mb = Musicbrainz(artist, title, acid_fps)
        primary = mb.primary_mb_release

        try:
            ar_id = primary["artsit-credit"][0]["artist"]["id"]
            al_id = primary["id"]
        except Exception as e:
            print(e)
            return None

        data = {"artist": ar_id, "album": al_id}
        return data

    @staticmethod
    def tag(filename: str, deezer: Deezer, ext: str) -> None:
        """ Function to write tags to the file, be it FLAC or MP3."""
        # retrieve tags

        if ext == ".mp3":
            Tag._tag_mp3(filename, deezer)
        else:
            raise NotImplementedError("Could not write tags. File extension not supported.")
