from .serverlist import ServerList


def setup(bot):
    bot.add_cog(ServerList(bot))
