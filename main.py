import multiprocessing
import signal

import utils
from models import chart, exception
from official_charts import Scraper

try:
    import download
except ImportError:
    raise NotImplementedError("downloader.py not found. Add to support downloading.")


MULTIPROCESS = True


def timeout_handler(signum: int, frame) -> None:  # type: ignore
    # No idea what the type of frame is.
    # It isn't that important but would be nice to know.
    raise exception.TimeoutException


def worker(chart_item: chart.ChartData) -> None:
    signal.alarm(1)
    print(f"{chart_item.chart_song.title} started.")
    try:
        d = chart_item.chart_song.to_deezer()
        dl = download.Download(d.track_id, f"{d.generate_filepath('/home/connor/UK Charts API Refactor/output')}", d)
        dl.download()
    except ValueError:
        print(f"{chart_item.chart_song.title} failed.")
        # Logic for failed to_deezer calls here.
    except exception.TimeoutException:
        print(f"{chart_item.chart_song.title} timed out.")
    finally:
        signal.alarm(0)
        return


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout_handler)
    # multiprocessing.set_start_method("spawn")
    for year in range(1954, 2020):
        dates = utils.generate_dates(year)
        for date in dates:
            s = Scraper(date, "singles-chart")
            if MULTIPROCESS:
                pool = multiprocessing.Pool()
                pool.map(worker, s.scrape())
                pool.close()
            else:
                for chart_item in s.scrape():
                    worker(chart_item)
