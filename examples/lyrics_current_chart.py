import official_charts
import datetime

from models import chart

scraper = official_charts.Scraper(datetime.datetime.now(), "singles-chart")

song: chart.ChartData
for song in scraper.scrape():
    deezer_song = song.to_deezer()
    lyrics = deezer_song.get_lyrics()
    print(f"Song ID: {deezer_song.track_id}")
    for line in lyrics:
        print(line)
    print("-" * 20)
