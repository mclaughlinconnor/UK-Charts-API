import datetime
from typing import Dict, List, Optional, Tuple, Union, Generator

import requests
from bs4 import BeautifulSoup as bs
import bs4
from tqdm import tqdm

import models


class Scraper:
    def __init__(self, date: datetime.datetime, chart_title: str):
        self.date: datetime.datetime = date
        self.chart_title: str = chart_title
        self.chart_id = self._chart_id_from_type(self.chart_title)
        self.chart_date = date.strftime("%Y%m%d")
        self.chart_url = self._chart_url(self.chart_title, self.chart_date, self.chart_id)

    def scrape(self) -> Generator[models.ChartData, None, None]:
        soup: bs = self.download_webpage(self.chart_url)

        rows: List[bs4.element.Tag]
        data_table: bs4.element.Tag
        rows, data_table = self._extract_rows(soup)
        for row in rows:
            if self._is_advertisement(row):
                continue
            chart_data = self.extract_data(row)
            stream_links = self._extract_stream_links(row, data_table)
            for link in stream_links:
                is_deezer_id = self._is_deezer_id(link)
                if is_deezer_id is not None and is_deezer_id:
                    deezer_stream_url = link
                if is_deezer_id is not None and not is_deezer_id:
                    spotify_stream_url = link
            chart_data.set_stream_urls(deezer_stream_url, spotify_stream_url)
            yield chart_data

    def _chart_id_from_type(self, chart_id: str) -> str:
        chart_ids = {"singles-chart": "7501"}
        return chart_ids[chart_id]

    def _is_advertisement(self, row: bs4.element.Tag) -> bool:

        if row.find(class_="adspace"):
            return True
        else:
            return False

    def _chart_url(self, chart_type: str, chart_date: str, chart_id: str) -> str:
        chart_url = f"http://www.officialcharts.com/charts/{chart_type}/{chart_date}/{chart_id}/"

        return chart_url

    def download_webpage(self, url: str) -> bs:
        page = requests.get(url)  # DLs the chart page
        soup = bs(page.content, "html.parser")  # Initialises into BS4

        return soup

    def _extract_rows(self, parsed_page: bs) -> Tuple[List[bs4.element.Tag], bs4.element.Tag]:
        data_table = parsed_page.find("table", class_="chart-positions")

        data_rows = data_table.find_all(
            "tr", class_=None
        )  # Creates a list of all the "Rows" of the tablespecial type of row

        return data_rows, data_table

    def _extract_stream_links(self, row: bs4.element.Tag, parsed_page: bs) -> List[str]:
        """ Finds all of the rows with streaming links in.
            Each of these has an index as part of their ID, get this.
        """
        try:
            # Gets all of the links, we only want the first (0th) one
            stream_open_button = row.find_all("div", class_="actions")[0].find_all("a", class_="")[0]

            # Splits the 'data-toggle' id into the hyphenated parts. Only the end part is unique
            stream_open_button_id: int = int(stream_open_button["data-toggle"].split("-")[3])
        except IndexError:
            # The open button doesn't exist in the row,
            # so there are no streaming links
            return []

        stream_elements = parsed_page.find_all("tr", class_=f"actions-view-listen-{stream_open_button_id}")
        stream_links: List[str] = [tag.get("href") for tag in stream_elements[0].find_all("a")]
        # Hopefully, if both Deezer and Spotify stream the song, a list of two links

        return stream_links

    def _is_deezer_id(self, link: str) -> Optional[bool]:
        if "deezer" in link:
            return True
        elif "spotify" in link:
            return False
        else:
            return None

    def add_stream_links_to_object(self, chart_data: models.ChartData, deezer: str, spotify: str) -> None:
        chart_data.set_stream_urls(deezer, spotify)

    def extract_data(self, row: bs4.element.Tag) -> models.ChartData:
        row_data: Dict[str, Union[str, int]] = {}

        row_data["title"] = row.find(class_="title").find("a").get_text()
        row_data["artist"] = row.find(class_="artist").find("a").get_text()
        row_data["position"] = row.find(class_="position").get_text()
        row_data["last_week"] = row.find(class_="last-week").get_text().strip()
        row_data["label"] = row.find(class_="label").get_text()
        row_data["peak"] = row.find_all("td", recursive=False)[3].get_text()
        row_data["woc"] = row.find_all("td", recursive=False)[4].get_text()

        return models.ChartData(row_data)


if __name__ == "__main__":
    scraper = Scraper(datetime.datetime.strptime("20021112", "%Y%m%d"), "singles-chart")
    i: models.ChartData
    for chart_data in tqdm(scraper.scrape()):
        print(chart_data.deezer_id)
