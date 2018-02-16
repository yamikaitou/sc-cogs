import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os


log = logging.getLogger("red.admin")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mycom(self, ctx, user: discord.Member=None):
        """This does stuff!"""

        #Your code will go here
        roles = ctx.message.server.roles
        json = """( "Count": {}, "Roles": [""".format(len(roles))
        for r in roles:
            if r.is_everyone:
                json += """( "Name": "everyone", "Position": {}, Permissions": ( 
                    "CREATE_INSTANT_INVITE": {},"KICK_MEMBERS": {},
                    "BAN_MEMBERS": {},"ADMINISTRATOR": {},
                    "MANAGE_CHANNELS": {},"MANAGE_GUILD": {},
                    "ADD_REACTIONS": {},"VIEW_AUDIT_LOG": {},
                    "VIEW_CHANNEL": {},"SEND_MESSAGES": {},
                    "SEND_TTS_MESSAGES": {},"MANAGE_MESSAGES": {},
                    "EMBED_LINKS": {},"ATTACH_FILES": {},
                    "READ_MESSAGE_HISTORY": {},"MENTION_EVERYONE": {},
                    "USE_EXTERNAL_EMOJIS": {},"CONNECT": {},
                    "SPEAK": {},"MUTE_MEMBERS": {},
                    "DEAFEN_MEMBERS": {},"MOVE_MEMBERS": {},
                    "USE_VAD": {},"CHANGE_NICKNAME": {},
                    "MANAGE_NICKNAMES": {},"MANAGE_ROLES": {},
                    "MANAGE_WEBHOOKS": {},"MANAGE_EMOJIS": {} ) )""".format(r.position, 
                    r.permissions.create_instant_invite,r.permissions.kick_members,
                    r.permissions.ban_members,r.permissions.administrator,
                    r.permissions.manage_channels,r.permissions.manage_server,
                    r.permissions.add_reactions,r.permissions.view_audit_logs,
                    r.permissions.read_messages,r.permissions.send_messages,
                    r.permissions.send_tts_messages,r.permissions.manage_messages,
                    r.permissions.embed_links,r.permissions.attach_files,
                    r.permissions.read_message_history,r.permissions.mention_everyone,
                    r.permissions.external_emojis,r.permissions.connect,
                    r.permissions.speak,r.permissions.mute_members,
                    r.permissions.deafen_members,r.permissions.move_members,
                    r.permissions.use_voice_activation,r.permissions.change_nickname,
                    r.permissions.manage_nicknames,r.permissions.manage_roles,
                    r.permissions.manage_webhooks,r.permissions.manage_emojis)
            else:
                json += """",( Name": "{}", "Position": {}, Permissions": ( 
                    "CREATE_INSTANT_INVITE": {},"KICK_MEMBERS": {},
                    "BAN_MEMBERS": {},"ADMINISTRATOR": {},
                    "MANAGE_CHANNELS": {},"MANAGE_GUILD": {},
                    "ADD_REACTIONS": {},"VIEW_AUDIT_LOG": {},
                    "VIEW_CHANNEL": {},"SEND_MESSAGES": {},
                    "SEND_TTS_MESSAGES": {},"MANAGE_MESSAGES": {},
                    "EMBED_LINKS": {},"ATTACH_FILES": {},
                    "READ_MESSAGE_HISTORY": {},"MENTION_EVERYONE": {},
                    "USE_EXTERNAL_EMOJIS": {},"CONNECT": {},
                    "SPEAK": {},"MUTE_MEMBERS": {},
                    "DEAFEN_MEMBERS": {},"MOVE_MEMBERS": {},
                    "USE_VAD": {},"CHANGE_NICKNAME": {},
                    "MANAGE_NICKNAMES": {},"MANAGE_ROLES": {},
                    "MANAGE_WEBHOOKS": {},"MANAGE_EMOJIS": {} ) )""".format(r.name, r.position, 
                    r.permissions.create_instant_invite,r.permissions.kick_members,
                    r.permissions.ban_members,r.permissions.administrator,
                    r.permissions.manage_channels,r.permissions.manage_server,
                    r.permissions.add_reactions,r.permissions.view_audit_logs,
                    r.permissions.read_messages,r.permissions.send_messages,
                    r.permissions.send_tts_messages,r.permissions.manage_messages,
                    r.permissions.embed_links,r.permissions.attach_files,
                    r.permissions.read_message_history,r.permissions.mention_everyone,
                    r.permissions.external_emojis,r.permissions.connect,
                    r.permissions.speak,r.permissions.mute_members,
                    r.permissions.deafen_members,r.permissions.move_members,
                    r.permissions.use_voice_activation,r.permissions.change_nickname,
                    r.permissions.manage_nicknames,r.permissions.manage_roles,
                    r.permissions.manage_webhooks,r.permissions.manage_emojis)
        
        json += """] )"""
        await self.bot.say(json)
    
    def _role_from_string(self, server, rolename, roles=None):
        if roles is None:
            roles = server.roles

        roles = [r for r in roles if r is not None]
        role = discord.utils.find(lambda r: r.name.lower() == rolename.lower(),
                                  roles)
        try:
            log.debug("Role {} found from rolename {}".format(
                role.name, rolename))
        except Exception:
            log.debug("Role not found for rolename {}".format(rolename))
        return role

def setup(bot):
    bot.add_cog(Yamik(bot))