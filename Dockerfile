FROM python:3.9.1-slim-buster
WORKDIR /app

ENV DISCORD_BOT_TOKEN="" \
    REDDIT_API_CLIENT_ID="" \
    REDDIT_API_CLIENT_SECRET="" \
    SUBREDDIT_SCRAPE_LIST="" \
    MEME_DOWNLOAD_DIR="" \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

RUN mkdir -p /memes/

COPY src/*.py ./
CMD /app/run.py
