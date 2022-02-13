import discord, asyncio
from discord.ext import commands
from ..config import *
from ..module import *

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="봇에게 디엠을 보내 문의하세요"))
        
def setup(bot):
    bot.add_cog(Activity(bot))