import discord
from discord import app_commands
import logging
from dotenv import load_dotenv
import os

# oh look! that's my script here
import functions

# create database if it doesn't already exist
functions.create_database()

# get token from .env
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# logging
handler = logging.FileHandler(filename='discord.log',encoding='utf-8',mode='w')

# specify intents
intents = discord.Intents.default()

# login
count_bot = discord.Client(intents=intents)
slash_commands = app_commands.CommandTree(count_bot)

# enable intents
intents.message_content = True
intents.members = True

# defining commands
@slash_commands.command(name="startcount", description="Start the count bot on this channel.")

async def startcount(interaction: discord.Interaction):
    await interaction.response.send_message("this is a message")

@count_bot.event
async def on_guild_remove(server):
    # remove them extra servers if bot removed
    functions.remove_server(server.id)

@count_bot.event
async def on_guild_join(server):
    # add new servers to the table
    functions.add_server(server.id)

@count_bot.event
async def on_ready():

    # slurp up them juicy server ids
    for server in count_bot.guilds:
        # now we add our slash commands to our stored servers
        guild = discord.Object(id=server.id)
        slash_commands.copy_global_to(guild=guild)
        await slash_commands.sync(guild=guild)

    # print when ready
    print(f"[count] {count_bot.user.name} is now active!")

# actually run the script :P
count_bot.run(token, log_handler=handler, log_level=logging.DEBUG)