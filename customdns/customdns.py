import discord
from discord.ext import commands
from discord import Embed
from __main__ import send_cmd_help
import asyncio
import aiodns
from cogs.utils.dataIO import dataIO
from cogs.utils import checks
from google.cloud import dns
from google.oauth2 import service_account
import os
import datetime


class CustomDNS:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(os.path.join("data", "dns", "settings.json"))
        self.gmod = dataIO.load_json(os.path.join("data", "dns", "gmod.json"))
        self.csgo = dataIO.load_json(os.path.join("data", "dns", "csgo.json"))
        self.tf2 = dataIO.load_json(os.path.join("data", "dns", "tf2.json"))
        self.unk = dataIO.load_json(os.path.join("data", "dns", "unk.json"))
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
    async def _dns(self, ctx):
        """Manage the DNS entries"""
        if checks.role_or_permissions(ctx, lambda r: r.name.lower() in ('monkey','server manager','owner')) is False:
            return False

        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)



    @_dns.command(pass_context=True, no_pm=True)
    async def nfo(self, ctx, sub, ident):
        """Create a DNS entry from an NFO name"""
        if checks.role_or_permissions(ctx, lambda r: r.name.lower() in ('monkey','server manager','owner')) is False:
            return False

        ip = await self.resolver.query("{}.game.nfoservers.com".format(ident), 'A')
        client = dns.Client(project=self.settings["project"][0], credentials=self.creds)
        zone = client.zone(self.settings['zone'][0], self.settings['domain'][0])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain'][0]), 'A', 60 * 60 * 2,
                                              [ip[0].host])
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()

        self.unk[sub] = {'dns':sub, 'nfo':ident, 'port':0, 'name':'unk'}
        dataIO.save_json(os.path.join("data", "dns", "unk.json"), self.unk)
        self.settings['last'] = int(datetime.datetime.utcnow().timestamp())
        dataIO.save_json(os.path.join("data", "dns", "settings.json"), self.settings)
        await self.bot.say("DNS Entry Created. Don't forget to update the server list, !serverlist edit {}".format(sub))

    @_dns.command(pass_context=True, no_pm=True)
    async def a(self, ctx, sub, ip):
        """Create or Modify a DNS A Record"""
        if checks.role_or_permissions(ctx, lambda r: r.name.lower() in ('monkey','server manager','owner')) is False:
            return False

        client = dns.Client(project=self.settings["project"][0], credentials=self.creds)
        zone = client.zone(self.settings['zone'][0], self.settings['domain'][0])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain'][0]), 'A', 60 * 60 * 2,
                                              [ip])
        changes = zone.changes()
        changes.add_record_set(record_set)
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()

        self.unk[sub] = {'dns':sub, 'nfo':ip, 'port': 0, 'name': 'unk'}
        dataIO.save_json(os.path.join("data", "dns", "unk.json"), self.unk)
        self.settings['last'] = int(datetime.datetime.utcnow().timestamp())
        dataIO.save_json(os.path.join("data", "dns", "settings.json"), self.settings)
        await self.bot.say("DNS Entry Created. Don't forget to update the server list if needed, !serverlist edit {}".format(sub))

    @commands.group(pass_context=True, no_pm=True, name="serverlist")
    async def serverlist(self, ctx):
        """Manage the DNS entries"""
        if ctx.invoked_subcommand is None:
            embed = Embed(colour=discord.Colour(0x426156), timestamp=datetime.datetime.utcfromtimestamp(self.settings['last']))

            embed.set_author(name="SuperCentral Server List", url="https://supercentral.co",
                             icon_url="https://supercentral.co/srvmgr/images/sclogo.jpg")
            embed.set_footer(text="Last Updated")

            if len(self.gmod) != 0:
                val = ""
                for server in self.gmod.items():
                    if server[1]['port'] not in (27015,0):
                        val += "{}.scgc.xyz - {}\n".format(server[1]['dns'], server[1]['name'])
                    else:
                        val += "{}.scgc.xyz:{} - {}\n".format(server[1]['dns'], server[1]['port'], server[1]['name'])

                embed.add_field(name="Garry's Mod - !gmod",
                                value=val,
                                inline=False)

            if len(self.csgo) != 0:
                val = ""
                for server in self.csgo.items():
                    if server[1]['port'] not in (27015,0):
                        val += "{}.scgc.xyz - {}\n".format(server[1]['dns'], server[1]['name'])
                    else:
                        val += "{}.scgc.xyz:{} - {}\n".format(server[1]['dns'], server[1]['port'], server[1]['name'])

                embed.add_field(name="Counter Strike Global Offensive - !csgo",
                                value=val,
                                inline=False)

            if len(self.tf2) != 0:
                val = ""
                for server in self.tf2.items():
                    if server[1]['port'] not in (27015,0):
                        val += "{}.scgc.xyz - {}\n".format(server[1]['dns'], server[1]['name'])
                    else:
                        val += "{}.scgc.xyz:{} - {}\n".format(server[1]['dns'], server[1]['port'], server[1]['name'])

                embed.add_field(name="Team Fortress 2 - !tf2",
                                value=val,
                                inline=False)

            if len(self.unk) != 0:
                val = ""
                for server in self.unk.items():
                    if server[1]['port'] != 0:
                        val += "{}.scgc.xyz - {}\n".format(server[1]['dns'], server[1]['name'])
                    else:
                        val += "{}.scgc.xyz:{} - {}\n".format(server[1]['dns'], server[1]['port'], server[1]['name'])

                embed.add_field(name="Undefined",
                                value=val,
                                inline=False)

            embed.add_field(name="Voice Servers - !voice",
                            value="discord.scgc.xyz - Discord (the one you are in)\nvoice.scgc.xyz - Teamspeak3",
                            inline=False)

            await self.bot.say(embed=embed)

    @serverlist.command(pass_context=True, no_pm=True)
    async def edit(self, ctx, sub, port, name, group, game):
        """Modify entries on the Server List"""
        if checks.role_or_permissions(ctx, lambda r: r.name.lower() in ('monkey','server manager','owner')) is False:
            return False



def check_folders():
    if not os.path.exists("data/dns"):
        print("Creating data/dns folder...")
        os.makedirs("data/dns")


def check_files():
    f = "data/dns/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's settings.json...")
        dataIO.save_json(f, {})

    f = "data/dns/gmod.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's gmod.json...")
        dataIO.save_json(f, {})

    f = "data/dns/csgo.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's csgo.json...")
        dataIO.save_json(f, {})

    f = "data/dns/tf2.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's tf2.json...")
        dataIO.save_json(f, {})

    f = "data/dns/unk.json"
    if not dataIO.is_valid_json(f):
        print("Creating default dns's unk.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(CustomDNS(bot))