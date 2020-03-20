class Insert:
    CHARTDATA = """
        INSERT INTO 'ChartData' (
            ChartID,
            ChartTitle,
            SongID,
            Position,
            Date,
            ChartURL,
            LastChartPosition)
        VALUES (?, ?, ?, ?, ?, ?, ?);"""

    MISSING = """INSERT INTO 'MissingSong' (
                     MissingID,
                     Title,
                     Artist,
                     Label,
                     WOC,
                     Peak,
                     ChartType)
                 VALUES (?, ?, ?, ?, ?, ?, ?);"""

    CHARTSONG = """INSERT INTO 'ChartSong' (
                       SongID,
                       Title,
                       Artist,
                       Label,
                       WOC,
                       PeakPos,
                       DeezerID,
                       SpotifyID)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""

    METADATA = """INSERT INTO 'Metadata' (
                      ISRC,
                      TitleShort,
                      TitleVersion,
                      Contributor,
                      ReleaseDate,
                      TrackNumber,
                      DiscNumber,
                      ExplicitLyrics,
                      BPM,
                      Gain)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""

    SONG = """INSERT INTO 'Song' (
                  SongID,
                  Title,
                  ArtistID,
                  ISRC,
                  Duration,
                  DeezerURL,
                  SpotifyID)
              VALUES (?, ?, ?, ?, ?, ?, ?);"""

    ARTIST = """INSERT INTO 'Artist' (
                    ArtistID,
                    Name,
                    ImageURL,
                    DeezerURL,
                    DeezerID)
                VALUES (?, ?, ?, ?, ?);"""

    SONGID = """SELECT SongID
                FROM 'ChartSong'
                WHERE Title = ? AND Artist = ?"""


class Update:
    UPDATE_WOC = """UPDATE ChartSong
                    WHERE SongID = ?
                    SET WOC = ?"""

    UPDATE_PEAK = """UPDATE ChartSong
                     WHERE SongID = ?
                     SET Peak = ?"""


class Select:
    CHARTDATA_BY_SONGID = """SELECT Peak, WOC
                        FROM 'ChartSong'
                        WHERE SongID = ?"""

    SONGID_BY_NAME = """SELECT SongID
                        FROM ChartSong
                        WHERE Title = ? AND Artist = ?"""

    TAG_DATA = """SELECT Song.ISRC,
                     TitleShort,
                     TitleVersion,
                     ReleaseDate,
                     TrackNumber,
                     DiscNumber,
                     ExplicitLyrics,
                     BPM,
                     Gain,
                     Lyrics,
                     Song.DeezerURL,
                     Artist.Name
                 FROM Metadata, Song, Artist
                 WHERE Metadata.ISRC = Song.ISRC AND Song.ArtistID = Artist.ArtistID;"""
