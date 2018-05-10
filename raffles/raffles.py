import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO, fileIO
from cogs.utils.chat_formatting import box, pagify
from __main__ import send_cmd_help, settings
from copy import deepcopy
import asyncio
import logging
import os
import aiomysql


log = logging.getLogger("red")
loop = asyncio.get_event_loop()

class Raffles:
    """Raffles!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/supercentral/settings.json")
        self.raffles = dataIO.load_json("data/raffles/raffles.json")

    @commands.group(pass_context=True, no_pm=True, name="raffle")
    async def raffle(self, ctx):


def check_folders():
    if not os.path.exists("data/supercentral"):
        print("Creating data/supercentral folder...")
        os.makedirs("data/supercentral")

    if not os.path.exists("data/raffles"):
        print("Creating data/raffles folder...")
        os.makedirs("data/raffles")


def check_files():
    f = "data/supercentral/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default supercentral/settings.json...")
        dataIO.save_json(f, {"host":"", "user":"", "pass":"", "data":""})

    f = "data/raffles/raffles.json"
    if not dataIO.is_valid_json(f):
        print("Creating default raffles/raffles.json...")
        dataIO.save_json(f, {})
    

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Raffles(bot))