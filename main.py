from official_charts import Scraper
import utils

try:
    import download
except ImportError:
    raise NotImplementedError("downloader.py not found. Add to support downloading.")
from models import chart

import multiprocessing


MULTIPROCESS = False


def worker(chart_item: chart.ChartData) -> None:
    print(f"{chart_item.chart_song.title} started.")
    try:
        d = chart_item.chart_song.to_deezer()
        dl = download.Download(d.track_id, f"{d.generate_filepath('/home/connor/UK Charts API Refactor/output')}", d)
        dl.download()
    except ValueError:
        print(f"{chart_item.chart_song.title} failed.")
        # Logic for failed to_deezer calls here.
        return


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
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
