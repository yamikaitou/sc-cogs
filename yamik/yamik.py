import discord
from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import dataIO, fileIO
from cogs.utils.chat_formatting import box, pagify
from copy import deepcopy
import asyncio
import logging
import os
import boto3


log = logging.getLogger("red")

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def mycom(self, ctx, user: discord.Member=None):
        """This does stuff!"""
        
        db = boto3.resource("dynamodb")
        table = db.Table("discord_groups")

        #Your code will go here
        roles = ctx.message.server.roles
        with table.batch_writer(overwrite_by_pkeys=['Name']) as batch:
            for r in roles:
                if r.is_everyone:
                    table.put_item(
                        Item={
                            'Name':'everyone',
                            'Position':r.position,
                            'Color':r.colour,
                            'Display':r.hoist,
                            'Mention':r.mentionable,
                            "CREATE_INSTANT_INVITE":r.permissions.create_instant_invite,
                            "KICK_MEMBERS":r.permissions.kick_members,
                            "BAN_MEMBERS":r.permissions.ban_members,
                            "ADMINISTRATOR":r.permissions.administrator,
                            "MANAGE_CHANNELS":r.permissions.manage_channels,
                            "MANAGE_GUILD":r.permissions.manage_server,
                            "ADD_REACTIONS":r.permissions.add_reactions,
                            "VIEW_AUDIT_LOG":r.permissions.view_audit_logs,
                            "VIEW_CHANNEL":r.permissions.read_messages,
                            "SEND_MESSAGES":r.permissions.send_messages,
                            "SEND_TTS_MESSAGES":r.permissions.send_tts_messages,
                            "MANAGE_MESSAGES":r.permissions.manage_messages,
                            "EMBED_LINKS":r.permissions.embed_links,
                            "ATTACH_FILES":r.permissions.attach_files,
                            "READ_MESSAGE_HISTORY":r.permissions.read_message_history,
                            "MENTION_EVERYONE":r.permissions.mention_everyone,
                            "USE_EXTERNAL_EMOJIS":r.permissions.external_emojis,
                            "CONNECT":r.permissions.connect,
                            "SPEAK":r.permissions.speak,
                            "MUTE_MEMBERS":r.permissions.mute_members,
                            "DEAFEN_MEMBERS":r.permissions.deafen_members,
                            "MOVE_MEMBERS":r.permissions.move_members,
                            "USE_VAD":r.permissions.use_voice_activation,
                            "CHANGE_NICKNAME":r.permissions.change_nickname,
                            "MANAGE_NICKNAMES":r.permissions.manage_nicknames,
                            "MANAGE_ROLES":r.permissions.manage_roles,
                            "MANAGE_WEBHOOKS":r.permissions.manage_webhooks,
                            "MANAGE_EMOJIS":r.permissions.manage_emojis
                        })
                else:
                    table.put_item(
                        Item={
                            'Name':r.name,
                            'Position':r.position,
                            'Color':r.colour,
                            'Display':r.hoist,
                            'Mention':r.mentionable,
                            "CREATE_INSTANT_INVITE":r.permissions.create_instant_invite,
                            "KICK_MEMBERS":r.permissions.kick_members,
                            "BAN_MEMBERS":r.permissions.ban_members,
                            "ADMINISTRATOR":r.permissions.administrator,
                            "MANAGE_CHANNELS":r.permissions.manage_channels,
                            "MANAGE_GUILD":r.permissions.manage_server,
                            "ADD_REACTIONS":r.permissions.add_reactions,
                            "VIEW_AUDIT_LOG":r.permissions.view_audit_logs,
                            "VIEW_CHANNEL":r.permissions.read_messages,
                            "SEND_MESSAGES":r.permissions.send_messages,
                            "SEND_TTS_MESSAGES":r.permissions.send_tts_messages,
                            "MANAGE_MESSAGES":r.permissions.manage_messages,
                            "EMBED_LINKS":r.permissions.embed_links,
                            "ATTACH_FILES":r.permissions.attach_files,
                            "READ_MESSAGE_HISTORY":r.permissions.read_message_history,
                            "MENTION_EVERYONE":r.permissions.mention_everyone,
                            "USE_EXTERNAL_EMOJIS":r.permissions.external_emojis,
                            "CONNECT":r.permissions.connect,
                            "SPEAK":r.permissions.speak,
                            "MUTE_MEMBERS":r.permissions.mute_members,
                            "DEAFEN_MEMBERS":r.permissions.deafen_members,
                            "MOVE_MEMBERS":r.permissions.move_members,
                            "USE_VAD":r.permissions.use_voice_activation,
                            "CHANGE_NICKNAME":r.permissions.change_nickname,
                            "MANAGE_NICKNAMES":r.permissions.manage_nicknames,
                            "MANAGE_ROLES":r.permissions.manage_roles,
                            "MANAGE_WEBHOOKS":r.permissions.manage_webhooks,
                            "MANAGE_EMOJIS":r.permissions.manage_emojis
                        })
                    
            
        
        
        await self.bot.say("Done")
    
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