import sqlite3
from datetime import date, timedelta
from typing import List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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

    @staticmethod
    def requests_retry_session(
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Tuple[int, int, int] = (500, 502, 504),
        session: Optional[requests.Session] = None,
    ) -> requests.Session:
        """Retrys a requests action a number of times

        Usage:
            req = requests_retry_session().get(url, stream=True)

        Keyword Arguments:
            retries {int} -- The number of times to retry (default: {3})
            backoff_factor {float} -- Time between retrys (see: https://urllib3.readthedocs.io/en/latest/reference/
                urllib3.util.html#module-urllib3.util.retry) (default: {0.3})
            status_forcelist {Tuple[int, int, int]} -- Status codes to force a rety for (default: {(500, 502, 504)})
            session {Optional[requests.Session]} -- The session to use, if none is specified, a new one will be created
                (default: {None})

        Returns:
            requests.Session -- [description]
        """
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
