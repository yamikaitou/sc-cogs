import discord
import random
from redbot.core import commands, Config, checks, utils


class ServerList(commands.Cog):
    """
    Game Server Listing
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=371963028, force_registration=True)
        self.config.register_guild(
            **{
                "types": [{"short": "voice", "long": "Voice Servers"}],
                "games": {"voice": [{"address": "here", "name": "Discord"}]},
            }
        )

    @commands.group()
    async def slset(self, ctx):
        conf = await self.config.guild(ctx.guild).all()
        print(conf)

    @commands.command()
    async def serverlist(self, ctx):
        embed = discord.Embed()
        embed.color = random.randint(0x000000, 0xFFFFFF)
        embed.set_author(
            name="SuperCentral Server List",
            url="https://supercentral.co",
            icon_url="https://supercentral.co/srvmgr/images/sclogo.jpg",
        )
        types = await self.config.guild(ctx.guild).get_raw("types")
        for type in types:
            games = await self.config.guild(ctx.guild).games.get_raw(type["short"])
            val = ""
            for game in games:
                val += "{} - {}\n".format(game["address"], game["name"])

            embed.add_field(name=type["long"], value=val, inline=False)

        await ctx.send(embed=embed)
