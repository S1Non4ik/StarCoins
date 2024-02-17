import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *
import random

class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - Game is Load')

    @commands.slash_command(guild_ids=[guild], description='Choose - heads/tails')
    async def coinflip (self, choose: str,money: int, inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {inter.user.name}")
        result = cursor.fetchone()
        if not result is None:
            coin = ['heads','tails']
            list = random.choice(coin)
            if choose == list:
                win = (money*1.8) + result
                cursor.execute(f"UPDATE main SET balance='{win}' WHERE discord_nick={inter.user.name}")
                connection.commit()
                await inter.response.send_message(f"You win ! - {money*1.8}", ephemeral=True)
            else:
                loose = result - money
                cursor.execute(f"UPDATE main SET balance='{loose}' WHERE discord_nick={inter.user.name}")
                connection.commit()
                await inter.response.send_message(f"You loose ;c !", ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))