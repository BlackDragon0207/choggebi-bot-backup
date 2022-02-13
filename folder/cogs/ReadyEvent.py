from discord.ext import commands
from ..config import *
from ..module import *

class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('\n서버 별명 미적용 확인 중 . . .')
        l = []
        p = []

        for user in self.bot.get_guild(ModGuild).members:
            RoleCount = user.roles
            pas = True
            for i in RoleCount:
                if i.id in whitelist:
                    pas = False
                    p.append(user.name)
            
            if pas:
                if user.nick == None:
                    if not (user.name).isdigit():
                        nickname = await GenerateNickname()
                        await user.edit(nick=nickname)
                        p.append(user.name)
                else:
                    if not len(user.nick) == 6:
                        nickname = await GenerateNickname()
                        l.append(user.name)
                        await user.edit(nick=nickname)
                    if not (user.nick).isdigit():
                        nickname = await GenerateNickname()
                        l.append(user.name)
                        await user.edit(nick=nickname)
        print(f'총 {len(l)}명 적용 완료')

def setup(bot):
    bot.add_cog(Activity(bot))
