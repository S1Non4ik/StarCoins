import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *
import random
from datetime import date, timedelta


class CoinSelectDropdownView(disnake.ui.StringSelect):
    def __init__(self):
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
        choose = self.values[0]
        cursor.execute(F"SELECT bet FROM coin WHERE discord = '{inter.user.id}'")
        money = cursor.fetchone()[0]
        try:
            Now = date.today() + timedelta(1)
            cursor.execute(f"UPDATE coin SET date='{Now}' WHERE discord={inter.user.id}")
            connection.commit()
            coin = ['heads', 'tails']
            list = random.choice(coin)
            cursor.execute(f"SELECT balance FROM main WHERE discord={inter.user.id}")
            result = cursor.fetchone()
            if not result is None:
                cursor.execute(f"UPDATE coin SET bet='{money}' WHERE discord='{inter.user.id}'")
                connection.commit()
                if choose == list:
                    win = (money * 2) + result[0]
                    cursor.execute(f"UPDATE main SET balance='{win}' WHERE discord={inter.user.id}")
                    connection.commit()
                    await inter.response.send_message(f"You win ! - {money * 2}", ephemeral=True)
                else:
                    loose = result[0] - money
                    cursor.execute(f"UPDATE main SET balance='{loose}' WHERE discord={inter.user.id}")
                    connection.commit()
                    await inter.response.send_message(f"You loose ;c !", ephemeral=True)
        except Exception as ext:
            print(ext)


class CoiSelectDropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CoinSelectDropdownView())


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - Game is Load')

    @commands.slash_command(guild_ids=[guild], description='Choose - heads/tails')
    async def coinflip(self, money: int,inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT date FROM coin WHERE discord = '{inter.user.id}'")
        datebd = cursor.fetchone()[0]
        if date.today() > datebd or date.today() == datebd:
            cursor.execute(f"SELECT balance FROM main WHERE discord='{inter.user.id}'")
            babki = cursor.fetchone()[0]
            if babki < money or babki == money:
                cursor.execute(F"UPDATE coin SET bet='0' WHERE discord='{inter.user.id}'")
                connection.commit()
                cursor.execute(f"SELECT bet FROM coin WHERE discord='{inter.user.id}'")
                balance = cursor.fetchone()[0] + money
                if balance < 50 or balance == 50:
                    staff = balance + money
                    cursor.execute(F"UPDATE coin SET bet='{staff}' WHERE discord='{inter.user.id}'")
                    connection.commit()
                    view = CoiSelectDropdownView()
                    await inter.response.send_message(view=view, ephemeral=True)
                else:
                    await inter.response.send_message('You have overbid', ephemeral=True)
            else:
                await inter.response.send_message('you dont have enough money', ephemeral=True)
        else:
            await inter.response.send_message('It is too early! You can play tomorrow', ephemeral=True)




def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))