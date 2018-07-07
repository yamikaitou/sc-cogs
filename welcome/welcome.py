import discord


class Welcome:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        serv = member.server
        embed = discord.Embed(colour=discord.Colour(0x91022d),
                              description="Welcome to the SuperCentral Gaming Community Discord\n\nPlease read {} to learn more about our community\nGive yourself some roles in {}\nRequest answers to questions related to our community in {}\nReport rule violators on our servers in {}\nSocialize with other members of the community in {}\nWe hope you enjoy your stay here\n\nOh, and don't forget to introduce yourself in {}".format(serv.get_channel("192701949575954435"),serv.get_channel("451147557607833600"),serv.get_channel("318204253791584268"),serv.get_channel("383405657161990145"),serv.get_channel("192153663555371008"),serv.get_channel("350900912887431178")))

        await self.bot.send_message(serv.get_channel("350900912887431178"), content="Greetings {} :wave:".format(member.mention), embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
