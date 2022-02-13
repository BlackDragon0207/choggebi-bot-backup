from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import textwrap, requests, io, discord
from ..config import *
from ..module import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        UserNickList = []
        astr = member.name
        guildname = member.guild.name
        buffer = io.BytesIO()
        buffer1 = io.BytesIO()

        for users in member.guild.members:
            if not users.nick == None:
                UserNickList.append(users.nick)
        while True:
            nickname = await GenerateNickname()
            if not nickname in UserNickList:
                await member.edit(nick=nickname)
                break
        


        para = textwrap.wrap(astr+'님,', width=15)
        Lpara = textwrap.wrap(guildname+' 에 오신것을 환영합니다.', width=100)

        MAX_W, MAX_H = 700, 300
        im = Image.open(Images+'background.png')
        im2 = Image.open(requests.get(member.avatar_url, stream=True).raw).convert('RGBA')
        im2 = im2.resize((135, 135))
        bigsize = (im2.size[0] * 3, im2.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(im2.size, Image.ANTIALIAS)
        im2.putalpha(mask)
        im.paste(im2,(283,43),im2)
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(Images+'Medium.ttf', 30)
        Lfont = ImageFont.truetype(Images+'Light.ttf', 22)
        current_h, pad = 34, 34
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text(((MAX_W - w) / 2, 190), line, font=font)
            current_h += h + pad
        for line in Lpara:
            w, h = draw.textsize(line, font=Lfont)
            draw.text(((MAX_W - w) / 2, 235), line,(205, 205, 205), font=Lfont)
            current_h += h + pad

        im.save(buffer,format='png')
        im.save(buffer1,format='png')
        buffer.seek(0)
        buffer1.seek(0)
        await member.guild.get_channel(JoinLog).send(file=discord.File(buffer, f'{member.id}.png'))

        rulechannel = member.guild.get_channel(844455206296223745)
        embed = discord.Embed(title=f'{member.guild.name}, 어서오세요!',color=0x8AF362,description=f'{member.mention}님, 서버에서 활동하시기 전 \n{rulechannel.mention}을 확인해 주세요!')
        embed.set_image(url=f"attachment://{member.id}.png")
        await member.send(file=discord.File(buffer1, f'{member.id}.png'),embed=embed)



def setup(bot):
    bot.add_cog(Events(bot))
