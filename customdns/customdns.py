import discord
from discord.ext import commands
from __main__ import send_cmd_help
import asyncio
import aiodns
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from google import cloud
from google.oauth2 import service_account
import os

class CustomDNS:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(os.path.join("data", "dns", "settings.json"))
        self.creds = service_account.Credentials.from_service_account_file(os.path.join("data", "dns", "gcloud.json"))
        loop = asyncio.get_event_loop()
        self.resolver = aiodns.DNSResolver(loop=loop)
            
    @commands.group(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def dnsconfig(self, ctx):
        """Config GCloud DNS settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Project: {}\nDomain: {}\nZone: {}".format(self.settings['project'][0], self.settings['domain'][0], self.settings['zone'][0]))
            
    @dnsconfig.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def project(self, ctx, *value):
        """Set the Project-ID"""
        self.settings["project"] = value
        dataIO.save_json(os.path.join("data", "dns", "settings.json"), self.settings)
            
    @dnsconfig.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def domain(self, ctx, *value):
        """Set the Domain """
        self.settings["domain"] = value
        dataIO.save_json(os.path.join("data", "dns", "settings.json"), self.settings)
            
    @dnsconfig.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def zone(self, ctx, *value):
        """Set the Zone"""
        self.settings["zone"] = value
        dataIO.save_json(os.path.join("data", "dns", "settings.json"), self.settings)

    @commands.group(pass_context=True, no_pm=True, name="dns")
    @checks.serverowner_or_permissions(administrator=True)
    async def _dns(self, ctx):
        """Manage the DNS entries"""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
    
    @_dns.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def nfo(self, ctx, ident, sub):
        """Create a DNS entry from an NFO name"""
        
        ip = await self.resolver.query("{}.game.nfoservers.com".format(ident), 'A')
        client = cloud.dns.Client(project=self.settings["project"][0], credentials=self.creds)
        zone = client.zone(self.settings['zone'][0], self.settings['domain'][0])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain'][0]), 'A', 60*60*2, [ip[0].host])
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()
        await self.bot.say("DNS Entry Created")
        

def check_folders():
    if not os.path.exists("data/dns"):
        print("Creating data/dns folder...")
        os.makedirs("data/dns")


def check_files():

    f = "data/dns/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's settings.json...")
        dataIO.save_json(f, {})

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CustomDNS(bot))