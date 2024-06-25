import discord
import os
from dotenv import load_dotenv
import random
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

welcome_channels = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('+ping'):
        await message.channel.send('Apne Kaam Se Kaam Rakh')
    elif message.content.startswith('+bol'):
        await message.channel.send('Bakwas Band Kar')
    elif message.content.startswith('+set'):
        try:
            channel_id = int(message.content.split()[1].strip('<#').strip('>'))  # Extract channel ID
            welcome_channels[message.guild.id] = channel_id
            await message.channel.send(f'Welcome channel set to <#{channel_id}>')
        except (IndexError, ValueError):
            await message.channel.send('Invalid command usage. Please use `+set #channel_id`')

@client.event
async def on_member_join(member):
    channel = client.get_channel(welcome_channels.get(member.guild.id))
    if channel:
        await channel.send(f'Welcome {member.mention} to the server!')
    elif member.guild.system_channel:
        await member.guild.system_channel.send(f'Welcome {member.mention} to the server!')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(welcome_channels.get(member.guild.id))
    if channel:
        await channel.send(f'{member.name} has left the server. We Will Miss You!.')
    elif member.guild.system_channel:
        await member.guild.system_channel.send(f'{member.name} has left the server. We Will Miss You!.')


client.run(TOKEN)