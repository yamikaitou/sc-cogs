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
import boto3
import aiomysql


log = logging.getLogger("red")
loop = asyncio.get_event_loop()

class Yamik:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot
        self.db = boto3.resource("dynamodb")
        self.settings = dataIO.load_json("data/sc-perms/settings.json")

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
            await self.bot.say("Truncating Table")
            await cur.execute("TRUNCATE discord_groups")
            await conn.commit()
            
            await self.bot.say("Dumping Roles")
            roles = ctx.message.server.roles
            for r in roles:
                sname = None
                if r.is_everyone:
                    sname = 'everyone'
                else:
                    sname = r.name
                
                await cur.execute("""INSERT INTO discord_groups VALUES ( "{}",{},"{}",{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{} )""".format(
                    sname,r.position,r.colour,r.hoist,r.mentionable,
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
        
        await self.bot.say("Done")
    
    
    @perms.command(pass_context=True, no_pm=True)
    async def push2(self, ctx, user: discord.Member=None):
        """Erases and pushes current Discord Roles and Permissions to AWS"""
        
        await self.bot.say("Deleting Table")
        table = self.db.Table("discord_groups")
        table.delete()
        
        table.meta.client.get_waiter('table_not_exists').wait(TableName='discord_groups')
        await self.bot.say("Creating table")
        table = self.db.create_table(
            TableName='discord_groups',
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
            AttributeDefinitions=[
                {
                    'AttributeName': 'Name',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'Position',
                    'AttributeType': 'N'
                },
        
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        table.meta.client.get_waiter('table_exists').wait(TableName='discord_groups')
        await self.bot.say("Dumping Roles")

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
        
def check_folders():
    folders = ("data", "data/sc-perms/")
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    if not os.path.isfile("data/sc-perms/settings.json"):
        print("Creating empty data/sc-perms/settings.json")
        dataIO.save_json("data/sc-perms/settings.json", """{ "host":"", "user":"", "pass":"", "data":"" }""")
    

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Yamik(bot))