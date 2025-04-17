import os

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from dotenv import load_dotenv

import yt_dlp
import requests

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix = '/', intents = intents)

@bot.event
async def on_ready():
    print("bot started")

@bot.command()
async def play(ctx, *, query):
	
	bot_voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
	if bot_voice_client and bot_voice_client.is_playing():
		bot_voice_client.stop()
    
	FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
	video, source = search(query)
	print(source)
  
	connected_to_voice_channel = False
	bot_voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
	
	if ctx.author.voice:		#if sender is in a voice channel
		if bot_voice_client and bot_voice_client.is_connected():	#if bot is in a voice channel
			await bot_voice_client.move_to(ctx.author.voice.channel)
			connected_to_voice_channel = True
		else:
			bot_voice_client = await ctx.author.voice.channel.connect()
			connected_to_voice_channel = True

	if connected_to_voice_channel:
		bot_voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))


@bot.command()
async def stop(ctx):
	bot_voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
	if bot_voice_client and bot_voice_client.is_playing():
		bot_voice_client.stop()
	

def search(query):
    with yt_dlp.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True' '--verbose'}) as ydl:
        try: requests.get(query)
        except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else: info = ydl.extract_info(query, download=False)
    return (info, info['url'])

bot.run(BOT_TOKEN)
