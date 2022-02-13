from discord.ext import commands
import discord
from ..config import *
from ..module import *

ModMailList = []
ModChannel = []

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
         await ctx.send(f'**```[ 다시 시도하셔도 이 오류가 뜨시면 관리자에게 문의해주세요. ]\n📰 {error}```**')
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.MissingRequiredArgument):
         await ctx.send(f'**```[ 알 수 없는 오류 ( 권한 문제 ) ]\n📰 {error}```**')

    @commands.command(name='경고',aliases=['warning'],description='경고를 추가합니다.')
    async def warning(self, ctx, user: discord.Member):
        if not ctx.author.guild_permissions.manage_guild:return
        
        WarningRole1 = ctx.guild.get_role(WarningLevel1)
        WarningRole2 = ctx.guild.get_role(WarningLevel2)
        WarningRole3 = ctx.guild.get_role(WarningLevel3)

        if WarningRole1 in user.roles:
            EmbedColor = WarningRole2.color
            await user.add_roles(WarningRole2)
            await user.remove_roles(WarningRole1)

            text = '누적 경고가 1회 있습니다.\n 경고 2 회가 누적되었습니다.\n`경고 추가 + 1`'
        elif WarningRole2 in user.roles:
            EmbedColor = WarningRole3.color
            await user.add_roles(WarningRole3)
            await user.remove_roles(WarningRole2)

            text = '누적 경고가 2회 있습니다.\n 경고 3 회가 누적되었습니다.\n`경고 추가 + 1`\n\n>>> 경고 1회가 추가된다면 서버에서 추방 당합니다.'#3렙
        elif WarningRole3 in user.roles:
            EmbedColor = 0x2F3136

            text = '누적 경고가 3회가 누적되어 서버에서 밴 처리합니다.'
            await user.ban(reason='경고 4회 누적')
        else:
            await user.add_roles(WarningRole1)
            EmbedColor = WarningRole1.color
            
            text = '경고 1 회가 누적되었습니다.\n`경고 추가 + 1`'

        embed = discord.Embed(title='✂ 관리자 명령어 ( 경고 )',description=user.mention+text,color=EmbedColor)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(ModMail(bot))