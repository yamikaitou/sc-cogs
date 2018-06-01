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
        await self.bot.say("Special delivery for {}, courtesy of Fish Prime (the freshest fish delivered anywhere)\n{} slaps {} with a large trout".format(victim.mention, author.mention, victim.mention))


def setup(bot):
    bot.add_cog(Trout(bot))
