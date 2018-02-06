import discord
from discord.ext import commands

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""

        #Your code will go here
        print(ctx.message.server.roles)
        #await self.bot.say()

def setup(bot):
    bot.add_cog(Yamik(bot))