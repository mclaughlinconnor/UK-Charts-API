import musicbrainzngs


class Musicbrainz:
    """ Class is used to make sure the release of the ID supplied as
        query_string is the main one.
    """

    def __init__(self, artist: str, title: str, acid_results: dict) -> None:
        musicbrainzngs.set_useragent("UK Chart Scraper", 1.0)

        self.acid_results = acid_results
        self.artist = artist
        self.title = title
        # self.acoustid_recording_ids = [x["id"] for x in acid_results["results"][0]["recordings"]]
        self.mb_releases = self._mb_search(self.artist, self.title)

        self.primary_mb_release = self.mb_releases[0]

    def _mb_search(self, artist: str, title: str) -> list:
        possible_recordings = musicbrainzngs.search_recordings(
            query=f'title:"{title}" AND artistname:"{artist}" AND primarytype:"Album" AND status:"Official"', limit=100
        )["recording-list"]

        final_releases: list = []

        for recording in possible_recordings:
            for release in recording["release-list"]:
                if "secondary-type-list" not in release["release-group"]:
                    if len(final_releases) == 0:
                        final_releases.append(release)
                    else:
                        final_releases = self._sort_countries(final_releases, release)

        return final_releases

    def _sort_countries(self, final_releases: list, release: dict) -> list:
        """ Favours British releases, then European, then everywhere else."""
        if release["country"] == "GB":
            release_list_index = 0
            while release["date"] >= final_releases[release_list_index]["date"]:
                release_list_index += 1
            final_releases.insert(release_list_index, release)
        elif release["country"] == "XE":
            release_list_index = 0
            while final_releases[release_list_index]["country"] == "GB":
                release_list_index += 1
            final_releases.insert(release_list_index, release)
        else:
            final_releases.append(release)

        return final_releases
