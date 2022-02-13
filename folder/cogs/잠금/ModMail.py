from discord.ext import commands
import discord, datetime, aiofiles
from ..config import *
from ..module import *

ModMailList = []
ModChannel = []

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='닫기',aliases=['close'],description='문의 채널을 닫는 명령어입니다.')
    async def close(self, ctx):
        if ctx.author.bot: return
        if not isinstance(ctx.channel, discord.channel.DMChannel): 
            if not ctx.channel.id in ModChannel: return
            ModChannel.remove(ctx.channel.id)
            Guild = ctx.channel.guild
            ModUser = Guild.get_member(int(ctx.channel.topic))
            ModMailList.remove(ModUser.id)
            await ctx.channel.delete()

            embed2 = discord.Embed(color=0x8AF362,timestamp=datetime.datetime.utcnow())
            embed2.set_author(name=f'{ctx.author.name}님이 티켓을 닫았습니다.',icon_url=ctx.author.avatar_url)
            await ModUser.send(embed=embed2)

            Log = Guild.get_channel(ModLog)
            await Log.send(f'```diff\n- {ctx.author.name} / {ModUser.name}({ModUser.id}) 티켓 닫음```')

    @commands.command(name='블랙',aliases=['black'],description='제작중 - 다시는 문의를 못하게 하는 명령어입니다.')
    async def blacklist(self, ctx):
        if ctx.author.bot: return
        if not isinstance(ctx.channel, discord.channel.DMChannel): 
            if not ctx.channel.id in ModChannel: return
            ModUser = ctx.channel.topic

            async with aiofiles.open(ModBlackFile, mode='a',encoding='UTF-8') as f:
                await f.write(ModUser)
                await f.write('\n')
                await f.close()

            ModChannel.remove(ctx.channel.id)
            Guild = ctx.channel.guild
            ModUser = Guild.get_member(int(ctx.channel.topic))
            ModMailList.remove(ModUser.id)
            await ctx.channel.delete()
            embed2 = discord.Embed(color=0x000000,timestamp=datetime.datetime.utcnow(),description='당신은 블랙리스트입니다.')
            embed2.set_author(name=f'{ctx.author.name}님이 티켓을 닫았습니다.',icon_url=ctx.author.avatar_url)
            await ModUser.send(embed=embed2)

            Log = Guild.get_channel(ModLog)
            await Log.send(f'```diff\n> {ctx.author.name} / {ModUser.name}({ModUser.id}) 블랙리스트```')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot: return
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if ctx.channel.id in ModChannel:
                if ctx.content.startswith('ㅊ!') or ctx.content.startswith('초!') or ctx.content.startswith('cho!'):
                    return
                    
                Guild = ctx.channel.guild
                ModUser = Guild.get_member(int(ctx.channel.topic))

                embed2 = discord.Embed(description=ctx.content,color=0x2F3136,timestamp=datetime.datetime.utcnow())
                embed2.set_author(name=f'{ctx.author.name}님의 답변입니다.',icon_url=ctx.author.avatar_url)
                await ModUser.send(embed=embed2)

                Log = Guild.get_channel(ModLog)
                await Log.send(f'```md\n* {ctx.author.name} -> {ModUser.name}({ModUser.id}) 답변\n↳ {ctx.content}```')

            if isinstance(ctx.channel, discord.channel.DMChannel): 
                if ctx.author.id in ModMailList:
                    guild = self.bot.get_guild(ModGuild)
                    for i in guild.channels:
                        if str(i.name) == f'ㄴ문의｜{ctx.author.id}':
                            MailChannel = i
                            break
                    

                    await ctx.add_reaction('<:magic:848951892653637643>')

                    embed2 = discord.Embed(description=ctx.content,color=0x2F3136,timestamp=datetime.datetime.utcnow())
                    embed2.set_author(name=f'{ctx.author.name}님의 문의입니다.',icon_url=ctx.author.avatar_url)
                    await MailChannel.send(embed=embed2)

                    Log = guild.get_channel(ModLog)
                    await Log.send(f'```{ctx.author.name}({ctx.author.id}) 문의\n↳ {ctx.content}```')

        else:
            if isinstance(ctx.channel, discord.channel.DMChannel): 

                async with aiofiles.open(ModBlackFile, mode='r',encoding='UTF-8') as f:
                    BlackList = await f.read()
                    # print(BlackList)
                if str(ctx.author.id) in BlackList:
                    await ctx.author.send('**당신은 블랙리스트 유저입니다.**')
                    return

                ModMailList.append(ctx.author.id)

                await ctx.add_reaction('<:magic:848951892653637643>')

                guild = self.bot.get_guild(ModGuild)
                cat = discord.utils.get(guild.categories, name="📰 - 고객센터ㅣ")
                channel = await guild.create_text_channel(f'ㄴ문의｜{ctx.author.id}', category=cat)
                ModChannel.append(channel.id)
                await channel.edit(topic=ctx.author.id)

                embed1 = discord.Embed(title='티켓이 생성되었습니다.',description='기다리고 계시면 관리자 중 한 명이 답변해 줄 겁니다.',color=0x8AF362,timestamp=datetime.datetime.utcnow())
                await ctx.author.send(embed=embed1)

                embed2 = discord.Embed(description=ctx.content,color=0x8AF362,timestamp=datetime.datetime.utcnow())
                embed2.set_author(name=f'{ctx.author.name}님의 문의입니다.',icon_url=ctx.author.avatar_url)
                await channel.send(embed=embed2)

                Log = guild.get_channel(ModLog)
                await Log.send(f'```diff\n+ {ctx.author.name}({ctx.author.id}) 티켓 생성\n↳ {ctx.content}```')
        
def setup(bot):
    bot.add_cog(ModMail(bot))