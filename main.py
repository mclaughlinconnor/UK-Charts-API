import logging
import multiprocessing
import signal
from typing import Optional

import utils
from db import Db
from models import chart, exception
from official_charts import Scraper

try:
    import download
except ImportError:
    raise NotImplementedError("downloader.py not found. Add to support downloading.")


MULTIPROCESS = False
TIMEOUT = 45


def timeout_handler(signum: int, frame) -> None:  # type: ignore
    # No idea what the type of frame is.
    # It isn't that important but would be nice to know.
    raise exception.TimeoutException


def worker(chart_item: chart.ChartData) -> Optional[tuple]:
    signal.alarm(TIMEOUT)
    logging.info(f"{chart_item.chart_song.title} started.")
    try:
        deezer = chart_item.chart_song.to_deezer()
        track_download = download.Download(
            deezer.track_id, f"{deezer.generate_filepath('/home/connor/Python/UK Charts API Refactor/output')}", deezer
        )
        track_download.download()

        return deezer, chart_item, track_download
    except ValueError:
        logging.error(f"{chart_item.chart_song.title} failed.")
    except exception.TimeoutException:
        logging.warning(f"{chart_item.chart_song.title} timed out.")
    finally:
        signal.alarm(0)
        return None, None, None

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout_handler)
    logging.basicConfig(level=logging.WARN)

    database = Db("data/data.db")

    for year in range(1954, 2020):
        dates = utils.generate_dates(year)
        for date in dates:
            scraper = Scraper(date, "singles-chart")
            if MULTIPROCESS:
                pool = multiprocessing.Pool()
                for deezer, chart_item, track_download in pool.imap_unordered(worker, scraper.scrape()):
                    if any([deezer is None, chart_item is None]):
                        continue
                    deezer.write_record(database)
                    chart_item.write_record(database)
                    if track_download is not None:
                        track_download.write_record(database)
                    database.commit()
                pool.close()
            else:
                for chart_item in scraper.scrape():
                    deezer, chart_item, track_download = worker(chart_item)
                    if any([deezer is None, chart_item is None]):
                        continue
                    deezer.write_record(database)
                    chart_item.write_record(database)
                    if track_download is not None:
                        track_download.write_record(database, deezer.track.get_db_id(database))
                    database.commit()
