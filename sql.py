class Insert:
    """Insert statements for all tables will eventually be included here
    """

    pass


class Update:
    """All of the required update statements will be included here
    """

    pass


class Select:
    """Any needed select statements will be here
    """

    pass


class Create:
    chart = """CREATE TABLE "chart" (
        "chart_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"    TEXT NOT NULL,
        "url"    TEXT NOT NULL,
        "date"    TIMESTAMP NOT NULL
    )"""

    image = """CREATE TABLE "image_file" (
        "image_file_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "filepath"    TEXT NOT NULL UNIQUE,
        "width"    INTEGER NOT NULL,
        "height"    INTEGER NOT NULL
    )"""

    audio_file = """CREATE TABLE "audio_file" (
        "audio_file_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "filepath"    TEXT NOT NULL UNIQUE,
        "format"    TEXT NOT NULL CHECK(format="mp3" or "flac"),
        "bitrate"    INTEGER NOT NULL,
        "sample_rate"    INTEGER NOT NULL,
        "bits"    INTEGER NOT NULL,
        "channels"    INTEGER NOT NULL,
        "download_time"    TIMESTAMP NOT NULL
    )"""

    photo = """CREATE TABLE "photo" (
        "photo_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "thumbnail_id"    INTEGER,
        "small_id"    INTEGER,
        "medium_id"    INTEGER,
        "big_id"    INTEGER,
        "xl_id"    INTEGER,
        FOREIGN KEY("xl_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("big_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("medium_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("small_id") REFERENCES "image_file"("image_file_id"),
        FOREIGN KEY("thumbnail_id") REFERENCES "image_file"("image_file_id")
    )"""

    chart_track = """CREATE TABLE "chart_track" (
        "chart_track_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "chart_id"    INTEGER NOT NULL,
        "track_id"    INTEGER,
        "position"    INTEGER,
        "last_week"    INTEGER,
        "peak"    INTEGER,
        FOREIGN KEY("chart_id") REFERENCES "chart"("chart_id"),
        FOREIGN KEY("track_id") REFERENCES "track"("track_id")
    )"""

    contributor = """CREATE TABLE "contributor" (
        "contributor_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "deezer_id"    INTEGER UNIQUE,
        "spotify_id"    TEXT UNIQUE,
        "name"    TEXT,
        "deezer_fans"    INTEGER,
        "photo_id"    INTEGER UNIQUE,
        FOREIGN KEY("photo_id") REFERENCES "photo"("photo_id")
    )"""

    album = """CREATE TABLE "album" (
        "album_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "deezer_id"    INTEGER UNIQUE,
        "spotify_id"    TEXT UNIQUE,
        "primary_contributor"    INTEGER,
        "contributors"    TEXT,
        "genre"    INTEGER,
        "duration"    INTEGER,
        "release_date"    TIMESTAMP,
        "cover"    INTEGER UNIQUE,
        FOREIGN KEY("cover") REFERENCES "photo"("photo_id"),
        FOREIGN KEY("primary_contributor") REFERENCES "contributor"("contributor_id")
    )"""

    genre = """CREATE TABLE "genre" (
        "genre_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"    TEXT,
        "photo"    INTEGER,
        FOREIGN KEY("photo") REFERENCES "genre"("genre_id")
    )"""

    track = """CREATE TABLE "track" (
        "track_id"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        "isrc"    TEXT NOT NULL UNIQUE,
        "contributor_id"    INTEGER NOT NULL,
        "album_id"    INTEGER NOT NULL,
        "audio_file_id"    INTEGER UNIQUE,
        FOREIGN KEY("contributor_id") REFERENCES "contributor"("contributor_id"),
        FOREIGN KEY("album_id") REFERENCES "album"("album_id"),
        FOREIGN KEY("isrc") REFERENCES "track_metadata"("isrc")
    )"""

    track_metadata = """CREATE TABLE "track_metadata" (
        "isrc"    TEXT NOT NULL UNIQUE,
        "deezer_id"    INTEGER,
        "spotify_id"    INTEGER,
        "title"    TEXT,
        "short_title"    TEXT,
        "duration"    INTEGER,
        "track_number"    INTEGER,
        "deezer_rank"    INTEGER,
        "explicit"    INTEGER NOT NULL CHECK(explicit = 1 or explicit = 0),
        "bpm"    REAL,
        "deezer_preview"    TEXT,
        "lyrics"    TEXT,
        "label"    TEXT,
        PRIMARY KEY("isrc")
    )"""
