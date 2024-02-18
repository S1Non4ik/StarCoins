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
                label="heads",
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
                    emb = disnake.Embed(title='**💰 Welcome to Coin Flip! 💰**',
                                        description='Congratulations, you won!\n'
                                                    f'Your balance now = {win}✮',
                                        colour=disnake.Colour.gold())
                    await inter.response.send_message(embed=emb, ephemeral=True)
                else:
                    loose = result[0] - money
                    cursor.execute(f"UPDATE main SET balance='{loose}' WHERE discord={inter.user.id}")
                    connection.commit()
                    emb = disnake.Embed(title='**💰 Welcome to Coin Flip! 💰**',
                                        description='Unfortunately you lost\n'
                                                    f'Your balance now = {loose}✮',
                                        colour=disnake.Colour.gold())
                    await inter.response.send_message(embed=emb, ephemeral=True)
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
        emb = disnake.Embed(title='**💰 Welcome to Coin Flip! 💰**',
                            description='Choose between heads and tails and win a prize!\n'
                                        f'If luck is on your side you will win - {money*1.8}✮',
                            colour=disnake.Colour.gold())
        cursor.execute(f"SELECT date FROM coin WHERE discord = '{inter.user.id}'")
        datebd = cursor.fetchone()[0]
        if date.today() > datebd or date.today() == datebd:
            cursor.execute(f"SELECT balance FROM main WHERE discord='{inter.user.id}'")
            babki = cursor.fetchone()[0]
            if babki > money or babki == money:
                cursor.execute(F"UPDATE coin SET bet='0' WHERE discord='{inter.user.id}'")
                connection.commit()
                if money < 50 or money == 50:
                    cursor.execute(F"UPDATE coin SET bet='{money}' WHERE discord='{inter.user.id}'")
                    connection.commit()
                    view = CoiSelectDropdownView()
                    await inter.response.send_message(embed=emb, view=view, ephemeral=True)
                else:
                    await inter.response.send_message('You have overbid', ephemeral=True)
            else:
                await inter.response.send_message('you dont have enough money', ephemeral=True)
        else:
            await inter.response.send_message('It is too early! You can play tomorrow', ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description='tells you if you have a pickaxe or not')
    async def minepickaxe(self, inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT pickaxe FROM pickaxe WHERE discord = {inter.user.id}")
        result = cursor.fetchone()[0]
        if result == False:
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='Mining is a noble job, but do you have a pickaxe?\n'
                                            f'Answer - You dont have a pickaxe',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb)
        else:
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='Mining is a noble job, but do you have a pickaxe?\n'
                                            f'Answer - You have a pickaxe',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb)

    @commands.slash_command(guild_ids=[guild], description='asks you if you want to buy a pickaxe')
    async def minepickaxebuy(self, inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT balance FROM main WHERE discord = {inter.user.id}")
        money = cursor.fetchone()[0]
        if money > 62500 or money == 62500:
            aye = money - 62500
            cursor.execute(f"UPDATE main SET balance = '{aye}' WHERE discord='{inter.user.id}' ")
            cursor.execute(f"UPDATE pickaxe SET pickaxe = 'true' WHERE discord='{inter.user.id}' ")
            connection.commit()
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='Congratulations on your pickaxe purchase!\n',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb, ephemeral=True)
        else:
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='you dont have enough money to buy a pickaxe\n',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description='sell your pickaxe for 47500 starcoins')
    async def minepickaxesell(self, inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT pickaxe FROM pickaxe WHERE discord = {inter.user.id}")
        pikaxe = cursor.fetchone()[0]
        if pikaxe == True:
            cursor.execute(f"UPDATE pickaxe SET pickaxe = 'false' WHERE discord='{inter.user.id}'")
            connection.commit()
            cursor.execut(f"SELECT balance FROM main WHERE discord = '{inter.user.id}'")
            aye = cursor.fetchone()[0] + 47500
            cursor.execute(f"UPDATE main SET balance = '{aye}' WHERE discord='{inter.user.id}'")
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='You sold the pickaxe for 47500\n',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb, ephemeral=True)
        else:
            emb = disnake.Embed(title='**✮ Starcoins Bot ✮**',
                                description='you dont have a pickaxe to sell\n',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description='sell your pickaxe for 47500 starcoins')
    async def mine (self, inter: disnake.ApplicationCommandInteraction):
        pass








def setup(bot: commands.Bot):
    bot.add_cog(Game(bot))