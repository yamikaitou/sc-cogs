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

class Giveaway:
    """Giveaways!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/supercentral/settings.json")
        
    

def check_folders():
    folders = ("data", "data/supercentral/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    if not os.path.isfile("data/supercentral/settings.json"):
        print("Creating empty data/supercentral/settings.json")
        dataIO.save_json("data/supercentral/settings.json", """{ "host":"", "user":"", "pass":"", "data":"" }""")
    

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Giveaway(bot))