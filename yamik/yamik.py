import discord
from discord.ext import commands
from discord import Embed
from cogs.utils import checks
from cogs.utils.dataIO import dataIO, fileIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os
import boto3
import random


log = logging.getLogger("red")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
    
    async def on_reaction_add(self, reaction, user):
        print(reaction.message.content)
        
    async def on_reaction_remove(self, reaction, user):
        print(reaction.message.content)

    @commands.command(pass_context=True)
    async def mycom(self, ctx, user: discord.Member=None):
        """This does stuff!"""
        
        #channel = ctx.message.author.server.get_channel("351073050772635650")
        channel = ctx.message.author.server.get_channel("206642595949051904")
        #await self.bot.send_message(channel, "")
        #embed = Embed(title="Another Test", color=discord.Color(random.randrange(0x1000000)), description="This is a test of some random system. This is only a test 3")
        #await self.bot.send_message(channel, embed=embed)
        
        
        embed = Embed(title="Giveaway - Free Steam Key (Unknown Game)", color=discord.Color(random.randrange(0x1000000)), description="React with :tickets: to enter!\nTime remaining: 60 minutes 00 seconds\n")
        msg = await self.bot.say(":confetti_ball:   **GIVEAWAY!!!**   :gift:   {}".format(ctx.message.author.mention), embed=embed)
        await self.bot.add_reaction(msg, "🎟")
    
def setup(bot):
    bot.add_cog(Yamik(bot))