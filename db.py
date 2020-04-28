import sqlite3
from sql import Create
from typing import Tuple


class Db:
    def __init__(self, file_name: str) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(file_name)  # Creates/opens db
        self.conn.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.conn.cursor()
        self.create_tables()

    def commit(self) -> None:
        self.conn.commit()

    def select(self, sql: str, parameters: Tuple) -> None:
        self.cursor.execute(sql, parameters)

    def insert(self, sql: str, parameters: Tuple) -> None:
        self.cursor.execute(sql, parameters)

    def update(self, sql: str, parameters: Tuple) -> None:
        self.cursor.execute(sql, parameters)

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        self.cursor.execute(Create.chart)
        self.cursor.execute(Create.image_file)
        self.cursor.execute(Create.audio_file)
        self.cursor.execute(Create.photo)
        self.cursor.execute(Create.chart_track)
        self.cursor.execute(Create.contributor)
        self.cursor.execute(Create.album)
        self.cursor.execute(Create.genre)
        self.cursor.execute(Create.track)
        self.cursor.execute(Create.track_metadata)
