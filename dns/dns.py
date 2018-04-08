import discord
from discord.ext import commands
import asyncio

class dns:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json(os.path.join("data", "dns", "settings.json"))
        credentials = service_account.Credentials.from_service_account_file(os.path.join("data", "dns", "gcloud.json"))
            
    @commands.group(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def dns(self, ctx):
        """Config GCloud DNS settings"""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
            
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

    @commands.group(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def dns(self, ctx):
        """Manage the DNS entries"""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
    
    @dns.command(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def nfo(self, ctx, ident, sub)
        """Create a DNS entry from an NFO name"""
        
        ip_list = []
        ais = asyncio.get_event_loop().getaddrinfo("{}.game.nfoservers.com".format(indent),0,0,0,0)
        for result in ais:
          ip_list.append(result[-1][0])
        ip_list = list(set(ip_list))
        
        client = dns.Client(project=self.settings["project"], credentials=credentials)
        zone = client.zone(self.settings['zone'], self.settings['domain'])
        record_set = zone.resource_record_set('{}.{}.'.format(sub, self.settings['domain']), 'A', 60*60*2, [ip_list[0],])
        changes = zone.changes()
        changes.create()
        while changes.status != 'done':
            asyncio.sleep(60)
            changes.reload()
        await self.bot.say("DNS Entry Created")
        

def check_files():
    if not os.path.exists(os.path.join("data", "dns", "settings.json")):
        try:
            os.mkdir(os.path.join("data", "dns"))
        except FileExistsError:
            pass
        else:
            dataIO.save_json(os.path.join("data", "dns", "settings.json"), {})

def setup(bot):
    check_files()
    bot.add_cog(dns(bot))
    
    
import socket

ip_list = []
ais = socket.getaddrinfo("www.yahoo.com",0,0,0,0)
for result in ais:
  ip_list.append(result[-1][0])
ip_list = list(set(ip_list))