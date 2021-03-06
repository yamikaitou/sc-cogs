import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO, fileIO
from cogs.utils.chat_formatting import box, pagify
from __main__ import send_cmd_help, settings
from copy import deepcopy
import asyncio
import logging
import os
import aiomysql


log = logging.getLogger("red")
loop = asyncio.get_event_loop()

class scperms:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json("data/supercentral/settings.json")

    @commands.group(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def perms(self, ctx):
        """Manages permissions and groups sync."""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
    
    @perms.command(pass_context=True, no_pm=True)
    async def push(self, ctx, user: discord.Member=None):
        """Erases and pushes current Discord Roles and Permissions to SQL"""
        
        conn = await aiomysql.connect(host=self.settings['host'], port=3306,
                                      user=self.settings['user'], password=self.settings['pass'], db=self.settings['data'],
                                      loop=loop)
    
        async with conn.cursor() as cur:
            await cur.execute("TRUNCATE discord_groups")
            await conn.commit()
            
            roles = ctx.message.server.roles
            for r in roles:
                sname = None
                if r.is_everyone:
                    sname = 'everyone'
                else:
                    sname = r.name
                
                await cur.execute("""INSERT INTO discord_groups VALUES ( {},"{}",{},"{}",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{} )""".format(
                    r.id,sname,r.position,r.colour,r.hoist,r.mentionable,
                    r.permissions.create_instant_invite,r.permissions.kick_members,r.permissions.ban_members,r.permissions.administrator,
                    r.permissions.manage_channels,r.permissions.manage_server,r.permissions.add_reactions,r.permissions.view_audit_logs,
                    r.permissions.read_messages,r.permissions.send_messages,r.permissions.send_tts_messages,r.permissions.manage_messages,
                    r.permissions.embed_links,r.permissions.attach_files,r.permissions.read_message_history,r.permissions.mention_everyone,
                    r.permissions.external_emojis,r.permissions.connect,r.permissions.speak,r.permissions.mute_members,
                    r.permissions.deafen_members,r.permissions.move_members,r.permissions.use_voice_activation,r.permissions.change_nickname,
                    r.permissions.manage_nicknames,r.permissions.manage_roles,r.permissions.manage_webhooks,r.permissions.manage_emojis
                    ))
            await conn.commit()
        
        
        
        
        conn.close()
        
        await self.bot.say("{} roles uploaded".format(len(roles)))
        
def check_folders():
    folders = ("data", "data/supercentral/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    if not os.path.isfile("data/supercentral/settings.json"):
        print("Creating empty data/supercentral/settings.json")
        dataIO.save_json("data/supercentral/settings.json", """{ "host":"", "user":"", "pass":"", "data":"" }""")
    

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(scperms(bot))