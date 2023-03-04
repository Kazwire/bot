import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

# Load our .env file
load_dotenv()

import sys, traceback

# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ["cogs.proxy", "cogs.admin", "cogs.premium"]

bot = commands.Bot(description="Proxy bot.", command_prefix="?", intents=discord.Intents.default())

@bot.event
async def on_ready():
    for extension in initial_extensions:
        try:
            print(f"Loading extension {extension}.")
            await bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}.", file=sys.stderr)
            traceback.print_exc()
    
    """http://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready"""

    print(
        f"\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n"
    )
    print(f"Successfully logged in and booted...!")

    await bot.tree.sync(guild=discord.Object(id=os.getenv("GUILD_ID")))


bot.run(
    os.getenv("TOKEN"),
    reconnect=True,
)

