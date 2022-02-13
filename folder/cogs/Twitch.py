from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
import textwrap, requests, io, discord, aiofiles
from ..config import *

font = ImageFont.truetype(Images+'Medium.ttf', 26)

class TW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        twrole = message.channel.guild.get_role(844459143830175774)
        if twrole in message.author.roles:
            async with aiofiles.open(TwitchFile, mode='r',encoding='UTF-8') as f:
                TwitchList = await f.read()

            if not str(message.author.id) in str(TwitchList):
                async with aiofiles.open(TwitchFile, mode='a',encoding='UTF-8') as f:
                    await f.write(str(message.author.id))
                    await f.write('\n')
                    await f.close()
                buffer2 = io.BytesIO()
                buffer3 = io.BytesIO()

                platform = '트위치'
                color_rgb = (110, 88, 148)

                para = message.author.name+'님,'
                im = Image.open(Images+f'{platform}.png')
                te = ImageDraw.Draw(im) 
                im2 = Image.open(requests.get(message.author.avatar_url, stream=True).raw).convert('RGBA')
                im2 = im2.resize((100, 100))
                bigsize = (im2.size[0] * 3, im2.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask) 
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(im2.size, Image.ANTIALIAS)
                im2.putalpha(mask)

                try:
                    im.paste(im2,(30,50),im2)
                except:
                    im.paste(im2,(30,50))

                te.text((154, 72),para, font=font)
                te.text((154, 102),platform, font=font, fill = color_rgb)

                im.save(buffer2,format='png')
                im.save(buffer3,format='png')
                buffer2.seek(0)
                buffer3.seek(0)

                ch = message.channel.guild.get_channel(membership_log)
                await ch.send(file=discord.File(buffer3, f'{message.author.id}.png'))
        

def setup(bot):
    bot.add_cog(TW(bot))
