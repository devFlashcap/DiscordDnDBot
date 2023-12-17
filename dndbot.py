import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '/', intents = intents)

@bot.event
async def on_ready():
    print("bot started")

@bot.command()
async def play(ctx):
    """
    /play [YouTube URL]
    """
    print("fasz")

bot.run(BOT_TOKEN)