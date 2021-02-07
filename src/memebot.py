import datetime
import os
import pathlib
import random
import re

import discord


class MemeBot(discord.Client):
    VALID_CHANNELS = ['memes']
    MEME_COMMAND_RE = re.compile(r'^\s*!meme\s*$')

    def __init__(self, meme_download_dir):
        self.meme_download_dir = meme_download_dir
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
        if MemeBot.MEME_COMMAND_RE.match(message.content) is not None:
            self.log(f'Got meme request from {message.author.name}')
            meme_file = self.get_random_meme_file()
            if meme_file is None:
                self.log('No memes found to reply with')
                await message.channel.send('I\'m sorry. I couldn\'t find a meme for you.')
            else:
                self.log(f'Replying with meme {meme_file}')
                await message.channel.send(file=discord.File(meme_file))

    def get_random_meme_file(self):
        if not os.path.isdir(self.meme_download_dir):
            return None
        files = list(pathlib.Path(self.meme_download_dir).rglob('*.*'))
        if len(files) == 0:
            return None
        return random.choice(files)

    def log(self, message):
        print(f'[Meme Bot] [{datetime.datetime.now()}]: {message}')
