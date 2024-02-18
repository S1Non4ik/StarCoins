import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *
import random
from datetime import date, timedelta





class CoiSelectDropdownView(disnake.ui.StringSelect):
    def __init__(self,bot, money):
        self.bot = money
        self.bot = bot
        options = [
            disnake.SelectOption(
                label="eagle",
                description="Choose the side",
            ),
            disnake.SelectOption(
                label="tails",
                description="Choose the side"
            )
        ]
        super().__init__(
            placeholder="📃 Choose the side",
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, inter: disnake.MessageInteraction):
        try:
            cursor.execute(f"SELECT date FROM coin WHERE discord = '{inter.user.id}'")
            datebd = cursor.fetchone()[0]
            if date.today() > datebd or date.today() == datebd:
                cursor.execute(f"SELECT balance FROM main WHERE discord={inter.user.id}")
                result = cursor.fetchone()
                if not result is None:
                    Now = date.today() + timedelta(1)
                    cursor.execute(f"UPDATE coin SET date='{Now}' WHERE discord={inter.user.id}")
                    connection.commit()
                    coin = ['heads', 'tails']
                    list = random.choice(coin)
                    if choose == list:
                        win = (self.money * 2) + result[0]
                        cursor.execute(f"UPDATE main SET balance='{win}' WHERE discord={inter.user.id}")
                        connection.commit()
                        await inter.response.send_message(f"You win ! - {self.mone * 2}", ephemeral=True)
                    else:
                        loose = result[0] - self.mone
                        cursor.execute(f"UPDATE main SET balance='{loose}' WHERE discord={inter.user.id}")
                        connection.commit()
                        await inter.response.send_message(f"You loose ;c !", ephemeral=True)
            else:
                await inter.response.send_message('It is too early! You can play tomorrow', ephemeral=True)
        except Exception as ext:
            print(ext)


class CoiSelectDropdownView(disnake.ui.View):
    def __init__(self,bot):
        self.bot = bot
        super().__init__()
        self.add_item(CoinSelectDropdown())


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - Game is Load')

    @commands.slash_command(guild_ids=[guild], description='Choose - heads/tails')
    async def coinflip(self, money: int, inter: disnake.ApplicationCommandInteraction):
        view = CoiSelectDropdownView(money)
        await inter.response.send_message(view=view)




def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))