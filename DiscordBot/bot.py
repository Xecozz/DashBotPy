import discord
import asyncio
from discord.ext import commands, ipc
from discord.ext.ipc.server import Server
from discord.ext.ipc.objects import ClientPayload
import logging
import sqlite3

class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    green = "\x1b[0;32m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger("DiscordBot.bot")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)



db = sqlite3.connect("../db.sqlite3")
logger.info("Database connected")

# Info Server DB
DiscordBot_BotChannel = db.execute("CREATE TABLE IF NOT EXISTS DiscordBot_BotChannel (GUILDID INT PRIMARY KEY NOT NULL, LOGS_CH INT, ANNONCE_CH INT, BIENVENUE_CH INT, BIENVENUE_FIELD TEXT )")

#Members Managers DB
DiscordBot_ManageMembers_Bans = db.execute("CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Bans (GUILDID INT PRIMARY KEY NOT NULL, USERID INT  NOT NULL , REASON TEXT, DATE DATETIME  NOT NULL, MODERATOR INT  NOT NULL )")
DiscordBot_ManageMembers_Warns = db.execute("CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Warns (GUILDID INT PRIMARY KEY NOT NULL, USERID INT, WARNID INT  NOT NULL, REASON TEXT, DATE DATETIME NOT NULL, MODERATOR INT NOT NULL )")
DiscordBot_ManageMembers_Kicks = db.execute("CREATE TABLE IF NOT EXISTS DiscordBot_ManageMembers_Kicks (GUILDID INT PRIMARY KEY NOT NULL, USERID INT  NOT NULL, KICKID INT NOT NULL, REASON TEXT, DATE DATETIME NOT NULL, MODERATOR INT NOT NULL )")

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
        await my_bot.get_channel(1021750826856894474).send(f"{user['username']} ({user['id']}) vient de se connecter !")

    @Server.route()
    async def checkGuild(self, data: ClientPayload):
        guildid = data.guildId
        guild = my_bot.get_guild(guildid)
        if guild is None:
            return {"status": False}
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

if __name__ == "__main__":
    my_bot.run("MTAyMzI4NTE0NzY4MTk2MDA2OQ.GCnFcD.OWVtZo99J5D7XKi_IqNNtBwUHWDOV0Y5zSTExs")
    asyncio.run(my_bot.setup_hook())  # start the IPC Server
