import datetime
import os
import pathlib
import random
import re

import discord


class MemeBot(discord.Client):
    VALID_CHANNELS = ['memes']
    HELP_COMMAND_RE = re.compile(r'^\s*!help\s*$')
    MEME_COMMAND_RE = re.compile(r'^\s*!meme\s*$')
    DOMAN_COMMAND_RE = re.compile(r'^\s*!doman\s*$')
    HELP_TEXT = '\n'.join([
        'Available meme commands:',
        '!help - Shows this list of commands',
        '!meme - Responds with one of the internet\'s finest memes',
        '!doman - Responds with a random video from the world famous playlist John Doman\'s Personal Picks'
    ])

    def __init__(self, meme_download_dir, reddit_scraper, personal_picks_scraper):
        self.meme_download_dir = meme_download_dir
        self.reddit_scraper = reddit_scraper
        self.personal_picks_scraper = personal_picks_scraper
        super().__init__()
        self.log('Created Meme Bot')

    async def on_ready(self):
        activity = discord.Activity(
            name='Dank Memes',
            type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.channel.name not in MemeBot.VALID_CHANNELS:
            return
        if MemeBot.HELP_COMMAND_RE.match(message.content) is not None:
            self.log(f'Got help request from {message.author.name}')
            await message.channel.send(MemeBot.HELP_TEXT)
        elif MemeBot.MEME_COMMAND_RE.match(message.content) is not None:
            self.log(f'Got meme request from {message.author.name}')
            meme_file = self.reddit_scraper.get_random_meme_file()
            if meme_file is None:
                self.log('No memes found to reply with')
                await message.channel.send('I\'m sorry. I couldn\'t find a meme for you.')
            else:
                self.log(f'Replying with meme {meme_file}')
                await message.channel.send(file=discord.File(meme_file))
        elif MemeBot.DOMAN_COMMAND_RE.match(message.content) is not None:
            self.log(
                f'Got Johnathan Doman\'s Personal Picks request from {message.author.name}')
            video_url = self.personal_picks_scraper.get_random_video_url()
            if video_url is None:
                self.log('No video found to reply with')
                await message.channel.send('I\'m sorry. I don\'t have a personal pick for you right now.')
            else:
                self.log(f'Replying with meme {video_url}')
                await message.channel.send(video_url)

    def log(self, message):
        print(f'[Meme Bot] [{datetime.datetime.now()}]: {message}')
