import discord
from discord.ext import  commands

class XPSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            pass

def setup(bot):
    bot.add_cog(XPSystem(bot))
