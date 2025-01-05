import asyncio
import time
import discord
from discord.ext import commands
import youtube_dl
import music
import urllib
import re

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True


bot = commands.Bot(command_prefix='&', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hola(ctx):
    await ctx.send('tu nariz contra mis bolas')

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.author.voice.channel
        await channel.connect()

@bot.command()
async def ring(ctx):
    if  ctx.author.voice is not None:
        await ctx.send("You are not connected to a voice channel")
        return
    else:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio("Audio/NokiaRingtone.mp3"))
        await asyncio.sleep(5)
        await vc.disconnect()

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Music stopped and disconnected from the voice channel.")
    else:
        await ctx.send("I am not connected to a voice channel.")


def search(url):
    query_string = urllib.parse.urlencode({'search_query': url})
    htm_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    url = 'http://www.youtube.com/watch?v=' + search_results[0]
    return url
    

def extract(ctx, url):
    with youtube_dl.YoutubeDL() as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print(f"Error extracting info: {e}")
            return False
        return {
            'link': url,
            'source': info['formats'][0]['url'],
            'title': info['title']
        }

            

def play_song(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        ctx.voice_client.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e)) 

@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        await ctx.send("I am not connected to a voice channel.")
        return
    else:
        music.play_song(ctx, url)
        url = search(url)
        extract()
        play_song(url)

bot.run('MTI5MDcxMzU5MjAxMzc4NzI2OQ.GOUCL_.mHrTsv8Vyd2OPNvAAFMApjEgbVXcygQwTGWh0A')