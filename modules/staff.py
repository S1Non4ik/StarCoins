import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *


class Staff(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - Staff is Load')

    @commands.slash_command(guild_ids=[guild], description='set user balance ')
    async def setbalance(self, user: str, money: int, inter: disnake.ApplicationCommandInteraction):
        if disnake.utils.get(inter.user.roles, id=ModRole):
            try:
                channel = self.bot.get_channel(LogsChannel)
                user = user.replace("<", "").replace("@", "").replace(">", "")
                cursor.execute(f"UPDATE main SET balance='{money}' WHERE discord='{user}'")
                connection.commit()
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'Нou have set the balance - <@{user}> | User balance now- {money}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, phemeral=True)
                await channel.send(f'<@{inter.user.id}> have set the balance - {money}, '
                                   f'for the user - <@{user}>')
            except Exception as ext:
                print(ext)
        else:
            emb = disnake.Embed(title='📛 Error 📛',
                                description='```You dont have enough rights```',
                                color=disnake.Color.blurple())
            await inter.response.send_message(embed=emb)

    @commands.slash_command(guild_ids=[guild], description='check user balance')
    async def checkbalance(self, user: str, inter: disnake.ApplicationCommandInteraction):
        if disnake.utils.get(inter.user.roles, id=ModRole):
            channel = self.bot.get_channel(LogsChannel)
            try:
                user = user.replace("<", "").replace("@", "").replace(">", "")
                cursor.execute(f"SELECT balance FROM main WHERE discord = {user}")
                result = cursor.fetchone()
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'Balance of <@{user}> - {result}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, ephemeral=True)
                await channel.send(f'<@{inter.user.id}> check balance - {result}, for the user - <@{user}>')
            except Exception as ext:
                print(ext)
        else:
            emb = disnake.Embed(title='📛 Error 📛',
                                description='```You dont have enough rights```',
                                color=disnake.Color.blurple())
            await inter.response.send_message(embed=emb)

    @commands.slash_command(guild_ids=[guild], description='gives a user starcoins')
    async def spay(self, money: int, user: str, inter: disnake.ApplicationCommandInteraction):
        if disnake.utils.get(inter.user.roles, id=ModRole):
            channel = self.bot.get_channel(LogsChannel)
            try:
                user = user.replace("<", "").replace("@", "").replace(">", "")
                cursor.execute(f"SELECT balance FROM main WHERE discord = {user}")
                result = cursor.fetchone()
                aye = money + result[0]
                cursor.execute(f"UPDATE main SET balance = '{aye}' WHERE discord='{user}' ")
                connection.commit()
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'You added money - <@{user}> | User balance now- {aye}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, ephemeral=True)
                await channel.send(f'<@{inter.user.id}> added money- {result}, for the user - <@{user}>')
            except Exception as ext:
                print(ext)
        else:
            emb = disnake.Embed(title='📛 Error 📛',
                                description='```You dont have enough rights```',
                                color=disnake.Color.blurple())
            await inter.response.send_message(embed=emb)

    @commands.slash_command(guild_ids=[guild], description='takes a certain amount of starcoins')
    async def sdeduct(self, user: str, money: int, inter: disnake.ApplicationCommandInteraction):
        if disnake.utils.get(inter.user.roles, id=ModRole):
            channel = self.bot.get_channel(LogsChannel)
            try:
                user = user.replace("<", "").replace("@", "").replace(">", "")
                cursor.execute(f"SELECT balance FROM main WHERE discord = {user}")
                result = cursor.fetchone()
                aye = result[0] - money
                cursor.execute(f"UPDATE main SET balance='{aye}' WHERE discord='{user}'")
                connection.commit()
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'You took money - <@{user}> | User balance now- {aye}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, ephemeral=True)
                await channel.send(f"<@{inter.user.id}> took {money} starcoins from <@{user}>")
            except Exception as ext:
                print(ext)
        else:
            emb = disnake.Embed(title='📛 Error 📛',
                                description='```You dont have enough rights```',
                                color=disnake.Color.blurple())
            await inter.response.send_message(embed=emb)


def setup(bot: commands.Bot):
    bot.add_cog(Staff(bot))