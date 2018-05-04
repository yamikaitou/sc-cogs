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
import time

log = logging.getLogger("red")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
    
    async def on_reaction_add(self, reaction, user):
        if self.valid and reaction.message.id == self.msg.id and reaction.emoji == "🎟" and user.id != "206641182606884866":
            self.entries.append(user)
            print(self.entries)
        
    async def on_reaction_remove(self, reaction, user):
        if self.valid and reaction.message.id == self.msg.id and reaction.emoji == "🎟":
            self.entries.remove(user)
            print(self.entries)
    
    @commands.command(pass_context=True)
    async def mycom2(self, ctx, msg):
        channel = ctx.message.author.server.get_channel("192153663555371008")
        await self.bot.send_message(channel, msg)
    
    @commands.command(pass_context=True)
    async def mycom3(self, ctx):
        await bot.say(content="Garry's Mod\nttt.scgc.xyz - Trouble in Terrorist Town #1\nprop.scgc.xyz - PropHunt #1\n\nCounter Strike Global Offensive\nkz.scgc.xyz - KZ/Climb\njb.scgc.xyz - Jailbreak\n\nTeam Fortress 2\ntf2.scgc.xyz - Unknown\n\nTeamspeak 3\nvoice.scgc.xyz")

    @commands.command(pass_context=True)
    async def mycom4(self, ctx):
        embed = discord.Embed(title="Server List", colour=discord.Colour(0x426156), url="https://discordapp.com", timestamp=datetime.datetime.utcfromtimestamp(1525418280))

        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/9mm1HQh9TdVk8JuYgZQFiaUnUm0_8L0z2Nt6oW4zUqw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/206641182606884866/694c6bd61c8379a64e8302670b4f76e7.webp?width=80&height=80")
        embed.set_author(name="SuperCentral", url="https://discordapp.com", icon_url="https://images-ext-1.discordapp.net/external/9mm1HQh9TdVk8JuYgZQFiaUnUm0_8L0z2Nt6oW4zUqw/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/206641182606884866/694c6bd61c8379a64e8302670b4f76e7.webp?width=80&height=80")
        embed.set_footer(text="Last Updated")
        
        embed.add_field(name="Garry's Mod", value="ttt.scgc.xyz - Trouble in Terrorist Town #1\nprop.scgc.xyz - PropHunt #1")
        embed.add_field(name="Counter Strike  Global Offensive", value="kz.scgc.xyz - KZ/Climb\njb.scgc.xyz - Jailbreak")
        embed.add_field(name="Team Fortress 2", value="tf2.scgc.xyz - Unknown")
        embed.add_field(name="Voice Servers", value="discord.scgc.xyz - Discord (the one you are in)\nvoice.scgc.xyz - Teamspeak3")
        
        await bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def mycom(self, ctx, user: discord.Member=None):
        """This does stuff!"""
        
        #channel = ctx.message.author.server.get_channel("351073050772635650")
        channel = ctx.message.author.server.get_channel("206642595949051904")
        #await self.bot.send_message(channel, "")
        #embed = Embed(title="Another Test", color=discord.Color(random.randrange(0x1000000)), description="This is a test of some random system. This is only a test 3")
        #await self.bot.send_message(channel, embed=embed)
        
        await self.bot.say("Attention {}, a new Giveaway is starting!!!".format(ctx.message.author.mention))
        embed = Embed(title="Giveaway - Free Steam Key (Unknown Game)", color=discord.Color(random.randrange(0x1000000)), description="React with :tickets: to enter!\nTime remaining: **1** minutes **00** seconds\n")
        self.msg = await self.bot.say(":confetti_ball:   **GIVEAWAY!!!**   :gift:", embed=embed)
        await self.bot.add_reaction(self.msg, "🎟")
        self.valid = True
        self.countdown = time.time() + 60
        self.entries = []
        
        times = divmod(self.countdown - time.time(), 3600)
        while True:
            if times[0] < 0:
                break
            elif times[0] == 0 and times[1] <= 10:
                await asyncio.sleep(1)
            elif times[0] == 0 and times[1] <= 30:
                await asyncio.sleep(5)
            elif times[0] == 1 and times[1] >= 59:
                await asyncio.sleep(10)
            else:
                await asyncio.sleep(30)
            
            times = divmod(self.countdown - time.time(), 3600)
            embed = Embed(title="Giveaway - Free Steam Key (Unknown Game)", color=discord.Color(random.randrange(0x1000000)), description="React with :tickets: to enter!\nTime remaining: **{}** minutes **{}** seconds\n".format(int(times[0]), int(times[1])))
            await self.bot.edit_message(self.msg, ":confetti_ball:   **GIVEAWAY!!!**   :gift:", embed=embed)
        
        
        win = random.sample(self.entries,1)[0]
        embed = Embed(title="Giveaway - Free Steam Key (Unknown Game)", color=discord.Color(random.randrange(0x1000000)), description="Winner: {}".format(win.mention))
        await self.bot.edit_message(self.msg, ":confetti_ball:   **GIVEAWAY!!!**   :gift:", embed=embed)
        await self.bot.say(":tada: Congratulations  {}! Please respond to my DM within 6 hours to claim your prize".format(win.mention))
        self.valid = False
        await self.bot.send_message(win, "Respond with `!claim` to claim your winnings")
        
    @commands.command(pass_context=True)
    async def claim(self, ctx, user: discord.Member=None):
        await self.bot.say("Thanks")
    
def setup(bot):
    bot.add_cog(Yamik(bot))