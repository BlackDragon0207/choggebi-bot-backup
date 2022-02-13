import discord, os
from discord.embeds import Embed
from discord.ext import commands
from folder.config import *
# from discord_slash import SlashCommand

intents = discord.Intents.all()
bot = commands.Bot(command_prefix = ['cho!','초!','ㅊ!'], intents=intents)
# bot.remove_command('help')

cogs = []
num = 1

for filename in os.listdir("folder/cogs"):
    if filename.endswith('.py'):
        cogs.append(filename)
        bot.load_extension(f'folder.cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    global num
    print(f'{bot.user.name} 준비 됨, 총 {len(cogs)}개의 Cogs\n\n[ Files ]')
    for i in cogs:
        print(f' ㄴ {num}번째, {i}')
        num = num + 1


bot.run(Token)
