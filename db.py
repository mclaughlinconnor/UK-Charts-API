import sqlite3
from typing import Tuple


class Db:
    def __init__(self, file_name: str) -> None:
        self.conn: sqlite3.Connection = sqlite3.connect(file_name)  # Creates/opens db
        self.conn.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.conn.cursor()

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
