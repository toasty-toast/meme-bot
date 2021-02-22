import datetime
import random

import youtube_dl


class PersonalPicksScraper():
    """
    Scrapes the personal picks playist and provides access to the videos.

    Parameters
    ----------

    playlist_url:
        The URL of the YouTube playlist.
    """

    video_urls = []

    def __init__(self, playlist_url):
        self.playlist_url = playlist_url

    def reprocess_videos(self):
        """Retrieves the list of videso in the playlsit and caches the links to each video."""
        self.log('Reprocessing Johnathan Doman\'s Personal Picks')
        with youtube_dl.YoutubeDL({'logger': PersonalPicksScraper.SilentLogger()}) as ydl:
            playlist = ydl.extract_info(self.playlist_url, download=False, )
            self.video_urls = [
                f'https://www.youtube.com/watch?v={v["id"]}' for v in playlist['entries']]

    def get_random_video_url(self):
        """Returns a random URL from the personal picks playlist."""
        if len(self.video_urls) == 0:
            return None
        return random.choice(self.video_urls)

    def log(self, message):
        """
        Logs a message.

        Parameters
        ----------

        message:
            The message to log.
        """
        print(
            f'[Personal Picks Scraper] [{datetime.datetime.now()}]: {message}')

    class SilentLogger():
        """
        A logger for YouTube-DL that doesn't actually log anything.
        """

        def debug(self, msg):
            pass

        def warning(self, msg):
            pass

        def error(self, msg):
            pass
