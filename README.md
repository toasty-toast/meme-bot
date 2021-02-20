# Meme Bot

## Overview

This repository contains source for Meme Bot, a Discord bot written in Python that provides text commands to get various memes through Discord.

## Running the Bot

The bot can be run in any Python environment, but this repository includes a Dockerfile to run the bot in a Docker container.

The Docker image is publish on [DockerHub](https://hub.docker.com/r/toastytoast/meme-bot).

If running locally, you must install the dependencies from `requirements.txt`, ideally in a virtual environment.

```shell
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

The bot requires the following environment variables to function. These are required in both the local and Docker environments.

| Variable                    | Description                                                     |
|-----------------------------|-----------------------------------------------------------------|
| DISCORD_BOT_TOKEN           | The token used by the Discord bot to authenticate with Discord. |
| REDDIT_API_CLIENT_ID        | The Client ID used to authenticate with the Reddit API.         |
| REDDIT_API_CLIENT_SECRET    | The Client secret used to authenticate with the Reddit API.     |
| SUBREDDIT_SCRAPE_LIST       | A comma-separated list of subreddits to scrape for memes.       |
| MEME_DOWNLOAD_DIR           | The directory that can be used to cache downloaded memes.       |
| PERSONAL_PICKS_PLAYLIST_URL | The URL for the YouTube memes playlist.                         |


## Using the Bot

The bot will only respond to messages sent in chat channels that are called `memes`.

The following commands are available.

| Command | Description                                                         |
|---------|---------------------------------------------------------------------|
| !help   | Shows a list of available commands                                  |
| !meme   | Responds in Discord with a random meme                              |
| !doman  | Responds in Discord with a random video URL from the memes playlist |