from datetime import date, timedelta
from typing import List, Tuple
import sqlite3


class Utils:
    @staticmethod
    def generate_dates(year: int) -> List[str]:
        """[Generates a list of all the week beginings in year. Note: Weeks start on Sundays]

        Arguments:
            year {int} -- [The year to generate a list of dates for]

        Returns:
            List[str] -- [List of str representations of datetime.date objects for the year]
        """
        dates = []
        d = date(year, 1, 1)  # January 1st
        d += timedelta(days=6 - d.weekday())  # First Sunday
        while d.year == year:
            dates.append(d.strftime("%Y%m%d"))
            d += timedelta(days=7)
            if d.year != year:
                break
        return dates

    @staticmethod
    def open_db(file_name: str) -> Tuple[sqlite3.Cursor, sqlite3.Connection]:
        """Opens a DB and returns the cursor and connection

        Arguments:
            file_name {str} -- The filename to be opened

        Returns:
            Tuple[sqlite3.Cursor, sqlite3.Connection] -- A tuple of the cursor and the connection
        """
        db = sqlite3.connect(file_name)  # Creates/opens db
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        return cursor, db
