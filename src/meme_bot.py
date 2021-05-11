import datetime
import inspect
import os
import pathlib
import random
import re

import discord
from discord.ext import commands


class MemeBot(commands.Bot):
    """
    A discord bot that responds to various text commands with different memes.

    Parameters
    ----------

    reddit_scraper:
        The RedditScraper that provides access to the memes.
    personal_picks_scraper:
        The PersonalPicksScraper that provides access to the personal picks YouTube playlist.
    """

    def __init__(self, reddit_scraper, personal_picks_scraper):
        self.reddit_scraper = reddit_scraper
        self.personal_picks_scraper = personal_picks_scraper
        super().__init__(command_prefix="!", help_command=None)
        self.add_command(commands.Command(self.help, name='help',
                                          help='Shows this help message'))
        self.add_command(commands.Command(self.meme, name='meme',
                                          help='Responds with one of the internet\'s finest memes'))
        self.add_command(commands.Command(self.doman, name='doman',
                                          help='Responds with a video from Johnathan Doman\'s Personal Picks'))
        self.log('Created Meme Bot')

    async def on_ready(self):
        """Called when the bot is first readied."""
        activity = discord.Activity(
            name='Dank Memes',
            type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)

    async def help(self, ctx):
        """
        Handles the help command by responding with the list of available commands.

        Parameters
        ----------

        ctx:
            The context provided by the commands API.
        """
        commands = [
            self.get_command('doman'),
            self.get_command('help'),
            self.get_command('meme')
        ]
        name_col_length = max([len(c.name) for c in commands]) + 1
        help_lines = [
            f'\t{self.command_prefix}{c.name.ljust(name_col_length)} {c.help}' for c in commands]
        help_text = 'Meme Commands:\r\n' + '\r\n'.join(help_lines)
        await ctx.channel.send(f'```{help_text}```')

    async def meme(self, ctx):
        """
        Handles the meme command by responding with a random meme.

        Parameters
        ----------

        ctx:
            The context provided by the commands API.
        """
        self.log(f'Got meme request from {ctx.message.author.name}')
        meme_file = self.reddit_scraper.get_random_meme_file()
        if meme_file is None:
            self.log('No memes found to reply with')
            await ctx.channel.send('I\'m sorry. I couldn\'t find a meme for you.')
        else:
            self.log(f'Replying with meme {meme_file}')
            await ctx.channel.send(file=discord.File(meme_file))

    async def doman(self, ctx):
        """
        Handles the doman command by responding with a random video from the personal picks YouTube playlist.

        Parameters
        ----------

        ctx:
            The context provided by the commands API.
        """
        self.log(
            f'Got Johnathan Doman\'s Personal Picks request from {ctx.message.author.name}')
        video_url = self.personal_picks_scraper.get_random_video_url()
        if video_url is None:
            self.log('No video found to reply with')
            await ctx.channel.send('I\'m sorry. I don\'t have a personal pick for you right now.')
        else:
            self.log(f'Replying with meme {video_url}')
            await ctx.channel.send(video_url)

    def log(self, message):
        """
        Logs a message.

        Parameters
        ----------

        message:
            The message to log.
        """
        print(f'[Meme Bot] [{datetime.datetime.now()}]: {message}')
