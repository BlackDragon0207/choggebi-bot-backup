from discord.ext import commands
import discord, os, traceback
from ..config import *
from ..module import *

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload',aliases=['리로드','ㄹㄹㄷ'])
    async def reload(self, ctx):
        if not ctx.author.id == 435841275632287745:return
        load = []
        text = ''
        for filename in os.listdir("folder/cogs"):
            if filename.endswith('.py'):
                load.append(filename)
                text = text + filename + '\n'
                self.bot.unload_extension(f'folder.cogs.{filename[:-3]}')
                self.bot.load_extension(f'folder.cogs.{filename[:-3]}')

        embed = discord.Embed(title='🛠 개발자 도구 ( Reload )')
        embed.add_field(name='reload 결과',value=f'총 `{len(load)}`개',inline=False)
        embed.add_field(name='리스트',value=text,inline=False)
        await ctx.reply(embed=embed)

    @commands.command(name='eval',aliases=['이발'])
    async def _eval(self, ctx: commands.Context, *, arg):
        if not ctx.author.id == 435841275632287745:return
        try:
            rst = eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
        embed=discord.Embed(title='**🛠 개발자 도구 ( Eval ) **', description=evalout)
        await ctx.send(embed=embed)

    @commands.command(name='await')
    async def _await(self, ctx: commands.Context, *, arg):
        if not ctx.author.id == 435841275632287745:return
        try:
            rst = await eval(arg)
        except:
            evalout = f'📥INPUT: ```python\n{arg}```\n💥EXCEPT: ```python\n{traceback.format_exc()}```\n ERROR'
            print(traceback.format_exc())
            
        else:
            evalout = f'📥INPUT: ```python\n{arg}```\n📤OUTPUT: ```python\n{rst}```\n SUCCESS'
            print(rst)
            
        embed=discord.Embed(title='**🛠 개발자 도구 ( Await ) **',  description=evalout)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Development(bot))
