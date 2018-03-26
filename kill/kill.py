import os
import random
import discord
from .utils import checks
from discord.ext import commands
from cogs.utils.dataIO import dataIO


class Kill:
    def __init__(self, bot):
        self.bot = bot
        self.filename = 'data/kill/kill.json'
        self.kills = dataIO.load_json(self.filename)

    async def save_kills(self):
        dataIO.save_json(self.filename, self.kills)

    @commands.command(pass_context=True, no_pm=True, name='kill')
    async def _kill(self, context, victim: discord.Member):
        """Randomly chooses a kill."""
        server = context.message.server
        author = context.message.author
        if server.id in self.kills:
            x = list(self.kills[server.id].keys())
            if victim.id == author.id:
                message = 'Per the Laws of Robotics, I cannot allow you to kill yourself'
            elif victim.id == self.bot.user.id:
                message = 'My eyes glow bright red as he stares at the knife {killer} is holding. {killer2} wets their pants and runs away screaming for their mommy'.format(killer=author.mention, killer2=author.display_name)
            elif victim.id == '192153481165930496':
                message = '{killer} follows YamiKaitou down a dark alley. {killer2} rushes in for the kill but goes right through Yami as if he wasn\'t even there. {killer2} looks around confused. Yami appears behind {killer2} and smashes him with a very large hammer.'.format(killer=author.mention, killer2=author.display_name)
            elif victim.id == '132016351622594560':
                message = '{killer} eats a burrito'.format(killer=author.mention)
            #elif victim.id == '202998328152031232':
                #message = 'Bmann'
            #elif victim.id == '112483286625898496':
                #message = 'Mikel'
            else:
                message = self.kills[server.id][random.choice(x)]['text'].format(victim=victim.mention, killer=author.mention)
        else:
            message = 'I don\'t know how to kill yet. Use `{}addkill` to add kills.'.format(context.prefix)
        await self.bot.say(message)

    @commands.command(pass_context=True, name='removekill')
    @checks.mod_or_permissions(administrator=True)
    async def _removekill(self, context, name):
        """Remove a kill"""
        server = context.message.server
        if server.id not in self.kills or name.lower() not in self.kills[server.id]:
            message = 'I do not know `{}`'.format(name)
        else:
            del self.kills[server.id][name.lower()]
            await self.save_kills()
            message = 'Kill removed.'
        await self.bot.say(message)

    @commands.command(pass_context=True, name='addkill')
    @checks.mod_or_permissions(administrator=True)
    async def _addkill(self, context, name, *kill_text):
        """Variables:
        {killer} adds the name of the killer
        {victim} adds the name of the victim
        """
        server = context.message.server
        if server.id not in self.kills:
            self.kills[server.id] = {}
        if name.lower() not in self.kills[server.id]:
            try:
                int(name)
            except:
                self.kills[server.id][name.lower()] = {}
                self.kills[server.id][name.lower()]['text'] = ' '.join(kill_text)
                await self.save_kills()
                message = 'Kill added.'
            else:
                message = 'Name cannot be a number alone, it must contain characters.'
        else:
            message = 'This kill is already in here! perform `{}removekill <name>` to remove it.'.format(context.prefix)
        await self.bot.say(message)


def check_folder():
    if not os.path.exists('data/kill'):
        print('Creating data/kill folder...')
        os.makedirs('data/kill')


def check_file():
    data = {}
    f = 'data/kill/kill.json'
    if not dataIO.is_valid_json(f):
        print('Creating default kill.json...')
        dataIO.save_json(f, data)


def setup(bot):
    check_folder()
    check_file()
    n = Kill(bot)
    bot.add_cog(n)