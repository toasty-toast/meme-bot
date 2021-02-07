import datetime
import os
import pathlib
import requests
import shutil

import praw


class RedditScraper():
    REDDIT_USER_AGENT = 'discord:toasty-toast-meme-bot:v1.0.0'

    def __init__(self, client_id, client_secret, subreddits, meme_download_dir):
        self.client_id = client_id
        self.client_secret = client_secret
        self.subreddits = subreddits
        self.meme_download_dir = meme_download_dir
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=RedditScraper.REDDIT_USER_AGENT)

    def reprocess_memes(self):
        self.log('Beginning meme reprocessing')

        if not os.path.isdir(self.meme_download_dir):
            self.log(
                f'Meme download "{self.meme_download_dir}" directory does not exist')
            return

        for subreddit in self.subreddits:
            try:
                self.reprocess_subreddit(subreddit)
            except Exception as e:
                self.log(f'Error while processing /r/{subreddit}: {e}')

        self.log('Finished meme reprocessing')

        files = list(pathlib.Path(self.meme_download_dir).rglob('*.*'))
        self.log(f'Downloaded {len(files)} memes')

    def reprocess_subreddit(self, subreddit):
        download_dir = os.path.join(self.meme_download_dir, subreddit)

        if os.path.isdir(download_dir):
            self.log(f'Clearing download subdirectory {download_dir}')
            shutil.rmtree(download_dir)

        if not os.path.isdir(download_dir):
            try:
                os.mkdir(download_dir)
            except Exception as e:
                self.log(
                    f'Could not create download subdirectory {download_dir}')
                return

        self.log(f'Processing submissions for /r/{subreddit}')
        for submission in self.reddit.subreddit(subreddit).top('week', limit=50):
            if submission.is_self:
                continue

            download_url = submission.url
            if 'v.redd.it' in submission.url.lower():
                try:
                    download_url = submission.media['reddit_video']['fallback_url']
                except:
                    pass

            response = requests.get(download_url, allow_redirects=True)
            if not response.ok:
                self.log(f'Failed to download {download_url}')
                continue

            file_ext = self.get_file_ext_from_mime_type(
                response.headers.get('content-type'))
            if file_ext is None:
                self.log(
                    f'Unable do determine file type for {response.headers.get("content-type")}')
                continue

            target_file = os.path.join(
                download_dir, f'{submission.id}.{file_ext}')
            self.log(
                f'Downloading {download_url} to file {target_file}')
            with open(target_file, 'wb') as file:
                for block in response.iter_content(1024):
                    if not block:
                        break
                    file.write(block)

    def get_file_ext_from_mime_type(self, mime_type):
        if mime_type.lower() == 'image/jpeg':
            return 'jpeg'
        if mime_type.lower() == 'image/png':
            return 'png'
        if mime_type.lower() == 'image/gif':
            return 'gif'
        if mime_type.lower() == 'video/mp4':
            return 'mp4'
        return None

    def log(self, message):
        print(f'[Reddit Scraper] [{datetime.datetime.now()}]: {message}')
