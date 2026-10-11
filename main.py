import discord
from discord import app_commands
import logging
from dotenv import load_dotenv
import os

# oh look! those are my scripts here
import functions
import count

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
@slash_commands.command(name="startcount", description="Start the count bot in this channel.")

async def startcount(interaction: discord.Interaction):
    old = functions.set_count_channel(interaction.guild_id, interaction.channel_id)
    if old is None:
        message = "Counting will happen in this channel."
    if old != interaction.channel_id:
        message = "Migrating the count to this channel."
    else:
        # derp
        message = "This channel is already running the count :P"
    # actually send the set message
    await interaction.response.send_message(message)

@count_bot.event
async def on_message(message):
    # quick check to avoid crash
    if message.author.bot or message.guild is None:
        return
    row = functions.get_count(message.guild.id)
    if row is None or message.channel.id != row["count_channel_id"]:
        return
    result, number, user_id = count.check_count(
        row["current_count_number"],
        row["last_count_user_id"],
        message.author.id,
        message.content,
    )
    # ignore no number messages
    if result == "ignore":
        return
    # react to number messages
    if result == "ok":
        if result == "ok":
            # write changes to the db
            functions.save_success(message.guild.id, number, user_id)
            # check if the current number is higher than highscore
            if number > row["max_count"]:
                await message.add_reaction("☑️")
            else:
                await message.add_reaction("✅")
    else:
        # failing message
        await message.add_reaction("❌")
        record = functions.fail_count(message.guild.id)
        await message.channel.send(
        f"{message.author.mention} messed up. This server's record is {record}. The count starts at 1 again."
)

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