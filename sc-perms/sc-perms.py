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
        self.db = boto3.resource("dynamodb")

    @commands.group(pass_context=True, no_pm=True)
    @checks.serverowner_or_permissions(administrator=True)
    async def perms(self, ctx):
        """Manages permissions and groups sync."""
        if ctx.invoked_subcommand is None:
            server = ctx.message.server
            await send_cmd_help(ctx)
    
    
    @modset.command(pass_context=True, no_pm=True)
    async def push(self, ctx, user: discord.Member=None):
        """Erases and pushes current Discord Roles and Permissions to AWS"""
        
        deleteTable()
        createTable()
        table.meta.client.get_waiter('table_exists').wait(TableName='discord_groups')
        table = self.db.Table("discord_groups")
        

        #Your code will go here
        roles = ctx.message.server.roles
        with table.batch_writer() as batch:
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
    
    async def deleteTable(self):
        await self.bot.say("Deleting Table")
        return self.db.delete_table(TableName="discord_groups")
    
    
    async def createTable(self):
        waiter = self.db.get_waiter('table_not_exists')
        await self.bot.say("Creating table")
        table = self.db.create_table(
            TableName="discord_groups",
            KeySchema=[
                {
                    'AttributeName': 'Name',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'Position',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions= [
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Position',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )

def setup(bot):
    bot.add_cog(Yamik(bot))