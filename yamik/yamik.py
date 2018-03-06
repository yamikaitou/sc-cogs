import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO, fileIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os
import boto3


log = logging.getLogger("red")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mycom(self, ctx, user: discord.Member=None):
        """This does stuff!"""
        
        try:
            channel = ctx.message.author.server.get_channel("351073050772635650")
            msg = await self.bot.get_message(channel, "419216445319413764")
        except discord.NotFound:
            raise CaseMessageNotFound()
        except discord.Forbidden:
            raise NoModLogAccess()
        else:
            print(msg.reactions)
            
        await self.bot.say("Done")
    
def setup(bot):
    bot.add_cog(Yamik(bot))