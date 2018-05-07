import discord
from discord.ext import commands
from discord import Embed
from __main__ import send_cmd_help
import asyncio
import aiodns
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from google import cloud
from google.oauth2 import service_account
import os
import datetime


class CustomDNS:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(os.path.join("data", "dns", "settings.json"))
        self.slist = dataIO.load_json(os.path.join("data", "dns", "list.json"))
        self.creds = service_account.Credentials.from_service_account_file(os.path.join("data", "dns", "gcloud.json"))
        loop = asyncio.get_event_loop()
        self.resolver = aiodns.DNSResolver(loop=loop)

    @commands.group(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def dnsconfig(self, ctx):
        """Config GCloud DNS settings"""
        if ctx.invoked_subcommand is None:
            await self.bot.say(
                "Project: {}\nDomain: {}\nZone: {}".format(self.settings['project'][0], self.settings['domain'][0],
                                                           self.settings['zone'][0]))

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
    @checks.role_or_permissions(name="Server Manager")
    async def _dns(self, ctx):
        """Manage the DNS entries"""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)

    @_dns.command(pass_context=True, no_pm=True)
    @checks.role_or_permissions(name="Server Manager")
    async def nfo(self, ctx, ident, sub):
        """Create a DNS entry from an NFO name"""

        ip = await self.resolver.query("{}.game.nfoservers.com".format(ident), 'A')
        client = cloud.dns.Client(project=self.settings["project"][0], credentials=self.creds)
        zone = client.zone(self.settings['zone'][0], self.settings['domain'][0])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain'][0]), 'A', 60 * 60 * 2,
                                              [ip[0].host])
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()

        entry = []
        entry['name'] = sub
        entry['nfo'] = ident
        entry['port'] = 0
        entry['game'] = 'unk'
        entry['group'] = 'unk'
        self.slist['zone']['unk'].append(entry)
        dataIO.save_json(os.path.join("data", "dns", "list.json"), self.slist)
        await self.bot.say("DNS Entry Created. Don't forget to update the server list, !serverlist edit {}".format(sub))

    @_dns.command(pass_context=True, no_pm=True)
    @checks.role_or_permissions(name="Server Manager")
    async def a(self, ctx, ip, sub):
        """Create or Modify a DNS A Record"""

        client = cloud.dns.Client(project=self.settings["project"][0], credentials=self.creds)
        zone = client.zone(self.settings['zone'][0], self.settings['domain'][0])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain'][0]), 'A', 60 * 60 * 2,
                                              [ip])
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()

        entry = []
        entry['dns'] = sub
        entry['nfo'] = 'n/a'
        entry['port'] = 0
        entry['name'] = 'unk'
        entry['group'] = 'unk'
        self.slist['zone']['unk'].append(entry)
        dataIO.save_json(os.path.join("data", "dns", "list.json"), self.slist)
        await self.bot.say("DNS Entry Created. Don't forget to update the server list if needed, !serverlist edit {}".format(sub))

    @commands.group(pass_context=True, no_pm=True, name="serverlist")
    async def serverlist(self, ctx):
        """Manage the DNS entries"""
        if ctx.invoked_subcommand is None:
            embed = Embed(colour=discord.Colour(0x426156), timestamp=datetime.datetime.utcfromtimestamp(1525418280))

            embed.set_author(name="SuperCentral Server List", url="https://supercentral.co",
                             icon_url="https://supercentral.co/srvmgr/images/sclogo.jpg")
            embed.set_footer(text="Last Updated")

            if len(self.slist['zone']['gmod']) != 0:
                embed.add_field(name="Garry's Mod - !gmod",
                                value="ttt.scgc.xyz - Trouble in Terrorist Town #1\nprop.scgc.xyz - PropHunt #1",
                                inline=False)

            if len(self.slist['zone']['csgo']) != 0:
                embed.add_field(name="Counter Strike Global Offensive - !csgo",
                                value="kz.scgc.xyz - KZ/Climb\njb.scgc.xyz - Jailbreak",
                                inline=False)

            if len(self.slist['zone']['tf2']) != 0:
                embed.add_field(name="Team Fortress 2 - !tf2",
                                value="tf2.scgc.xyz - Unknown",
                                inline=False)

            if len(self.slist['zone']['unk']) != 0:
                embed.add_field(name="Undefined",
                                value="unk.scgc.xyz - Unknown",
                                inline=False)

            embed.add_field(name="Voice Servers - !voice",
                            value="discord.scgc.xyz - Discord (the one you are in)\nvoice.scgc.xyz - Teamspeak3",
                            inline=False)

            await self.bot.say(embed=embed)

    @serverlist.command(pass_context=True, no_pm=True)
    @checks.role_or_permissions(name="Server Manager")
    @checks.role_or_permissions(name="Owner")
    async def edit(self, ctx, sub, port, name, group, game):
        """Modify entries on the Server List"""

        await self.bot.say("You have access")

def check_folders():
    if not os.path.exists("data/dns"):
        print("Creating data/dns folder...")
        os.makedirs("data/dns")


def check_files():
    f = "data/dns/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's settings.json...")
        dataIO.save_json(f, {})

    f = "data/dns/list.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's list.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CustomDNS(bot))