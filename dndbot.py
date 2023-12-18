import os

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from dotenv import load_dotenv

from youtube_dl import YoutubeDL
import requests

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = '/', intents = intents)

@bot.event
async def on_ready():
    print("bot started")

@bot.command()
async def play(ctx, *, query):
    if ctx.author.voice:		#if sender is in a voice channel
        bot_voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
        if bot_voice_client and bot_voice_client.is_connected():
            await bot_voice_client.move_to(ctx.author.voice.channel)
        else:
            await ctx.author.voice.channel.connect()
    print(query)

bot.run(BOT_TOKEN)