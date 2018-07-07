import discord


class Welcome:
    def __init__(self, bot):
        self.bot = bot

    async def on_member_join(self, member):
        embed = discord.Embed(colour=discord.Colour(0x91022d),
                              description="Welcome to the SuperCentral Gaming Community Discord\n\nPlease read #welcome to learn more about our community\nGive yourself some roles in #verification\nRequest answers to questions related to our community in #support\nReport rule violators on our servers in #reports\nSocialize with other members of the community in #general\nWe hope you enjoy your stay here\n\nOh, and don't forget to introduce yourself in #introduction")

        await bot.send_message(member.server.get_channel("350900912887431178"), content="Greetings {} :wave:".format(member.mention), embed=embed)

def setup(bot):
    bot.add_cog(Welcome(bot))
