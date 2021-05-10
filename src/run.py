#!/usr/bin/env python

import os
import time
import threading

import schedule

from meme_bot import MemeBot
from reddit_scraper import RedditScraper
from personal_picks_scraper import PersonalPicksScraper


DISCORD_BOT_TOKEN_ENV = 'DISCORD_BOT_TOKEN'
REDDIT_API_CLIENT_ID_ENV = 'REDDIT_API_CLIENT_ID'
REDDIT_API_CLIENT_SECRET_ENV = 'REDDIT_API_CLIENT_SECRET'
SUBREDDIT_SCRAPE_LIST_ENV = 'SUBREDDIT_SCRAPE_LIST'
MEME_DOWNLOAD_DIR_ENV = 'MEME_DOWNLOAD_DIR'
PERSONAL_PICKS_PLAYLIST_URL_ENV = 'PERSONAL_PICKS_PLAYLIST_URL'


def main():
    """The main entrypoint for the meme bot program."""
    discord_bot_token = get_env_or_error(DISCORD_BOT_TOKEN_ENV)
    reddit_api_client_id = get_env_or_error(REDDIT_API_CLIENT_ID_ENV)
    reddit_api_client_secret = get_env_or_error(REDDIT_API_CLIENT_SECRET_ENV)
    subreddit_scrape_list = get_env_or_error(SUBREDDIT_SCRAPE_LIST_ENV)
    meme_download_dir = get_env_or_error(MEME_DOWNLOAD_DIR_ENV)
    personal_picks_playlist_url = get_env_or_error(
        PERSONAL_PICKS_PLAYLIST_URL_ENV)

    unique_subreddits = list(set(subreddit_scrape_list.split(',')))
    reddit_scraper = RedditScraper(
        reddit_api_client_id,
        reddit_api_client_secret,
        unique_subreddits,
        meme_download_dir)

    personal_picks_scraper = PersonalPicksScraper(personal_picks_playlist_url)

    schedule_thread = threading.Thread(
        target=run_scheduled_tasks,
        args=(reddit_scraper, personal_picks_scraper),
        daemon=True)
    schedule_thread.start()

    bot = MemeBot(reddit_scraper, personal_picks_scraper)
    bot.run(discord_bot_token)


def run_scheduled_tasks(reddit_scraper, personal_picks_scraper):
    """
    Runs the scheduled tasks for the program. This will block indefinitely.
    """
    schedule.every(1).days.do(reddit_scraper.reprocess_memes)
    schedule.every(1).days.do(personal_picks_scraper.reprocess_videos)
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_env_or_error(env_var):
    """
    Retrieves an environment variable and returns it, or exits the application if it is not found.

    Parameters
    ----------

    env_var:
        The name of the environment variable to get.
    """
    var = os.environ.get(env_var)
    if var is None or var == '':
        print(f'Missing required environment variable: {env_var}')
        exit(1)
    else:
        print(f'Environment variable {env_var} = {var}')
    return var


if __name__ == '__main__':
    main()
