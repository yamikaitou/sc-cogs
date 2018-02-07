import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os


log = logging.getLogger("red.admin")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mycom(self, ctx, rolename, user: discord.Member=None):
        """This does stuff!"""

        #Your code will go here
        roles = ctx.message.server.roles
        for r in roles:
            if r.name is "@everyone":
                await self.bot.say("everyone - {}".format(r.permissions.value))
            await self.bot.say("{} - {}".format(r.name, r.permissions.value))
        
        await self.bot.say("Done")
    
    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles

        roles = [r for r in roles if r is not None]
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        try:
            log.debug("Role {} found from rolename {}".format(
                role.name, rolename))
        except Exception:
            log.debug("Role not found for rolename {}".format(rolename))
        return role

def setup(bot):
    bot.add_cog(Yamik(bot))