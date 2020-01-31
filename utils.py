from datetime import date, timedelta
from typing import List


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
