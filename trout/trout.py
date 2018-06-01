import discord
from discord.ext import commands


class Trout:
    """Trout Slap!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True, name='slap')
    async def _slap(self, ctx, victim: discord.Member):
        """Slap someone with a trout"""
        author = ctx.message.author
        await self.bot.say("Special delivery for {}, courtesy of Fish Prime (the freshest fish delivered anywhere)\nI slap you with a large trout :fish:".format(victim.mention))


def setup(bot):
    bot.add_cog(Trout(bot))
