import disnake
from cfg.cfg import guild
from disnake.ext import commands


class Market(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - Market is Load')


def setup(bot: commands.Bot):
    bot.add_cog(Market(bot))