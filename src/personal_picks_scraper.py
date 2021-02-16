import datetime
import random

import youtube_dl


class SilentLogger():
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class PersonalPicksScraper():
    video_urls = []

    def __init__(self, playlist_url):
        self.playlist_url = playlist_url

    def reprocess_videos(self):
        self.log('Reprocessing Johnathan Doman\'s Personal Picks')
        with youtube_dl.YoutubeDL({'logger': SilentLogger()}) as ydl:
            playlist = ydl.extract_info(self.playlist_url, download=False, )
            self.video_urls = [
                f'https://www.youtube.com/watch?v={v["id"]}' for v in playlist['entries']]

    def get_random_video_url(self):
        return random.choice(self.video_urls)

    def log(self, message):
        print(
            f'[Personal Picks Scraper] [{datetime.datetime.now()}]: {message}')
