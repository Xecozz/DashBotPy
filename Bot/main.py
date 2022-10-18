from dataclasses import dataclass

import discord
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Le bot est prêt.")


@client.event
async def on_message(message: discord.Message):
    if message.author.id == client.user.id: return
    if message.content.lower() == "ping":
        await message.channel.send("pong")


@client.event
async def on_member_join(member: discord.Member):
    channel = client.get_channel(1021750826856894474)
    await channel.send(f"bienvenue {member.name}")


client.run("MTAyMzI4NTE0NzY4MTk2MDA2OQ.GCnFcD.OWVtZo99J5D7XKi_IqNNtBwUHWDOV0Y5zSTExs")


@dataclass
class Bot:
    userId: int
    guildId: int

    def get_guild(self):
        return client.get_guild(self.guildId)

    def get_member(self):
        guild = self.get_guild()
        return guild.get_member(self.userId)

    def sendMessage(self, channelId):
        member = self.get_member()
        client.get_channel(channelId).send(f"{member.name} s'est connecté au dashboard ({member.id})")