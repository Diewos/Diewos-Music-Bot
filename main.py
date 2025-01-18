import asyncio
import time
import discord
from discord.ext import commands
import youtube_dl
import music

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True


def get_token():
    with open('config.txt', 'r') as file:
        return file.read().replace('\n', '')

token = get_token()


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



bot.run('MTI5MDcxMzU5MjAxMzc4NzI2OQ.GOUCL_.mHrTsv8Vyd2OPNvAAFMApjEgbVXcygQwTGWh0A')