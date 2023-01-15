import sys
import os
import asyncio
from pathlib import Path

import discord
from discord.ext import commands, ipc
from discord.ext.ipc.server import Server
from discord.ext.ipc.objects import ClientPayload
import sqlite3
import environ



root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from packages.log import LogInit


logger = LogInit("DiscordBot.bot").logger

db = sqlite3.connect("db.sqlite3")
logger.info("Database connected")


# Members Managers DB
DiscordBot_ManageMembers_Bans = db.execute(
    "CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Bans (GUILDID INT PRIMARY KEY NOT NULL, USERID INT  NOT NULL , REASON TEXT, DATE DATETIME  NOT NULL, MODERATOR INT  NOT NULL )")
DiscordBot_ManageMembers_Warns = db.execute(
    "CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Warns (GUILDID INT PRIMARY KEY NOT NULL, USERID INT, WARNID INT  NOT NULL, REASON TEXT, DATE DATETIME NOT NULL, MODERATOR INT NOT NULL )")
DiscordBot_ManageMembers_Kicks = db.execute(
    "CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Kicks (GUILDID INT PRIMARY KEY NOT NULL, USERID INT  NOT NULL, KICKID INT NOT NULL, REASON TEXT, DATE DATETIME NOT NULL, MODERATOR INT NOT NULL )")


class MyBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()

        super().__init__(
            command_prefix="$.",
            intents=intents,
        )

        self.ipc = ipc.Server(self, secret_key="pynel")

    async def on_ready(self):
        """Called upon the READY event"""
        await self.wait_until_ready()
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} commands")
        except Exception as e:
            logger.error(e)
        logger.info("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        logger.info("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        logger.error(f"An error occurred in {endpoint}: {error}")

    async def setup_hook(self) -> None:
        await self.ipc.start()
        return

    # routes
    @Server.route()
    async def logUserConnection(self, data: ClientPayload):
        user = data.user
        await my_bot.get_channel(1043500614442831944).send(f"{user['username']} ({user['id']}) vient de se connecter !")

    @Server.route()
    async def checkGuild(self, data: ClientPayload):
        guildid = data.guildId
        guild = my_bot.get_guild(guildid)
        if guild is None:
            return {"status": False}
        return {"status": True}

    @Server.route()
    async def sendAnnonceMessage(self, data: ClientPayload):
        message = data.message
        guild_id = data.guildId
        channelId = db.execute(f"SELECT channel_annonce FROM Dashboard_channelsetup WHERE guild_id = {guild_id}").fetchone()

        if channelId is None:
            system_channel = my_bot.get_guild(data.guildId).system_channel
            await system_channel.send(f"Le channel d'annonce n'est pas configuré ! \n Annonce : {message}")
            return {"status": True, "message": "Le channel d'annonce n'est pas configuré !"}
        else:
            channel = my_bot.get_channel(channelId[0])
            if not channel:
                return {"status": False, "error": "Channel not found"}
            await channel.send(message)
            return {"status": True}

    @Server.route()
    async def getGuildInfo(self, data: ClientPayload):
        try:
            userid = data.userId
            guildid = data.guildId

            guild = my_bot.get_guild(guildid)
            if guild is None:
                return {"status": False, "message": "Guild not found !"}
            if guild.owner.id != userid:
                return {"status": False,
                        "message": "You are not the owner of this guild !" + f"{guild.owner.id} != {userid}"}

            online = 0
            bots = 0


            for member in guild.members:
                if member.status == discord.Status.online:
                    online += 1

                if member.bot:
                    bots += 1

            channelNames = []
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text:
                    channelNames.append({"name": channel.name, "id": channel.id})

            icon = str(guild.icon) if guild.icon is not None else None
            description = guild.description if guild.description is not None else None

            guildInfoDico = {
                "status": True,
                "name": guild.name,
                "id": guild.id,
                "memberCount": guild.member_count,
                "channelCount": len(guild.channels),
                "online": online,
                "bots": bots,
                "icon": icon,
                "description": description,
                "guild_created_at": guild.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "roles_count": len(guild.roles),
                "premium_tier": guild.premium_tier,
                "channels_count": len(guild.channels),
                "channels_names": channelNames,

            }

            return {"status": True, "guildInfo": guildInfoDico}

        except:
            return {"status": False, "message": "Une erreur est survenue. (Slug ERROR)"}


my_bot = MyBot()


@my_bot.tree.command(name="ping", description="Ping the bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong ! {interaction.user.mention}", ephemeral=True)

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=str( BASE_DIR/".env"))

Token = env("TOKEN")

if __name__ == "__main__":
    my_bot.run(token=Token)
    asyncio.run(my_bot.setup_hook())  # start the IPC Server
