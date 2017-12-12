import discord
import time
import os
import asyncio

    
class breaktheinternet:
    
    messages = [
    "WE HAVE *JUST* 48 HOURS TO #STOPTHEFCC and save the Internet. Take action now and spread the word: battleforthenet.com",
    "#NetNeutrality dies in 2 days unless we stop this. Contact Congress now: battleforthenet.com",
    "#NetNeutrality dies in 2 days unless we stop this. Call Congress now: 202-759-7766",
    "Everyone needs to know that Congress has stopped FCC votes before. They can stop Ajit Pai’s plan and save #netneutrality. Visit battleforthenet.com to make sure your lawmakers hear from you about this. It’s almost too late!",
    "███████ ███ ████ ████ ██ ███ ███ ██████████ ██ ████ ███ ████████ ████ ██ ███ █ ██ ██████. Please upgrade your Internet to see this message: battleforthenet.com",
    "THIS IS AN INTERNET EMERGENCY: Call Congress now to #StopTheFCC from killing net neutrality and destroying the Internet as we know it: battleforthenet.com ",
    "This message is being ██████ by your internet provider. Well, not yet. But, that's what will happen if we ████ #StopTheFCC. Congress can stop this. Take action now: battleforthenet.com",
    "You know what's not funny? Screwing over hundreds of millions of people on behalf of a few of the most unpopular companies in the world. #StopTheFCC: battleforthenet.com ",
    "Don't let the FCC #breaktheinternet. We can stop this: battleforthenet.com ",
    "This message is ██████████ by your Internet provider. Stop them: battleforthenet.com",
    "Keep the Internet weird, save #NetNeutrality: battleforthenet.com ",
    "Congress has oversight over the FCC and only they can stop them from killing #NetNeutrality. Call them now: battleforthenet.com/call",
    "Without #netneutrality, the Internet will be like cable TV... big companies -- not you -- decide what you see. Take action now: battleforthenet.com",
    "The people who literally invented the Internet are warning the FCC against killing net neutrality: https://pioneersfornetneutrality.tumblr.com/ Join the protest: breaktheinternetprotest.org",
    "Without #netneutrality, indie artists and musicians will struggle to be heard: http://www.rollingstone.com/music/news/net-neutrality-how-a-repeal-could-kill-artists-careers-w513787 Join the protest: https://www.battleforthenet.com/",
    "Millions of Internet users are asking about #NetNeutrality ahead of the FCC’s plan to repeal the rules on December 14th. Head to battleforthenet.com to see what it’s all about and what you can do about it. ",
    "IT’S NOT OVER UNTIL IT’S OVER. We have to shut down Congress with phone calls about #NetNeutrality. Use this easy tool to call your lawmakers now and demand they #StopTheFCC: battleforthenet.com ",
    "Remember—Congressional pressure has stopped the FCC before! To save #NetNeutrality & #StopTheFCC we have to force Congress to act. So tell your friends, family, neighbors, colleagues, frenemies, teachers... just. tell. everyone: BreakTheInternetProtest.org ",
    "The most powerful and hated companies in the US want to be the Internet gatekeepers. Join the protest to #BreakTheInternet and save net neutrality: BreakTheInternetProtest.org",
    "Time is running out to save the Internet, this is how we do it: BreakTheInternetProtest.org #StopTheFCC "
    ]
    
    def __init__(self, bot):
        self.bot = bot
        check_reminders(self)

    async def check_reminders(self):
        while self is self.bot.get_cog("breaktheinternet"):
            await self.bot.send_messaage(client.get_channel('yami-test-room')), random.choice(messages))
            await asyncio.sleep(5)
            

def setup(bot):
    bot.add_cog(breaktheinternet(bot))