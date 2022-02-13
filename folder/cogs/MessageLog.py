from discord.ext import commands
import discord 
from pytz import timezone
from datetime import datetime
from ..config import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:return
        embed = discord.Embed(timestamp=datetime.now(timezone('Asia/Seoul')),description=f'**유저**:{after.author.name} ( {after.author.mention} )\n**아이디**:{after.author.id}', colour=discord.Colour(0x7B56BA))
        embed.set_author(name=f'메시지 수정 로그', icon_url = before.author.avatar_url)
        embed.add_field(name='채널',value=after.channel.mention,inline=False)
        embed.add_field(name='수정 전',value=f'```{before.content}```',inline=False)
        embed.add_field(name='수정 후',value=f'```{after.content}```',inline=False)
        await before.channel.guild.get_channel(edit_channel).send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:return
        if message.content == '':return
        embed = discord.Embed(timestamp=datetime.now(timezone('Asia/Seoul')),description=f'**유저**:{message.author.name} ( {message.author.mention} )\n**아이디**:{message.author.id}', colour=discord.Colour(0xD84848))
        embed.add_field(name='채널',value=message.channel.mention,inline=False)
        embed.add_field(name='내용',value=f'```{message.content}```',inline=False)
        embed.set_author(name=f'메시지 삭제 로그', icon_url = message.author.avatar_url)
        await message.channel.guild.get_channel(delete_channel).send(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
