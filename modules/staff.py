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
        role = disnake.utils.get()
        channel = self.bot.get_channel(LogsChannel)
        cursor.execute(f"UPDATE main SET balance='{money}' WHERE discord_nick={user}")
        connection.commit()
        await inter.response.send_message(f'you have set the balance - {money}, for the user - <@{user}>', ephemeral=True)
        await channel.send(f'<@{inter.user.id}> have set the balance - {money}, for the user - <@{user}>')

    @commands.slash_command(guild_ids=[guild], description='check user balance')
    @commands.has_permissions(administrator=True)
    async def checkbalance(self, user:str , inter: disnake.ApplicationCommandInteraction):
        channel = self.bot.get_channel(LogsChannel)
        cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {user}")
        result = cursor.fetchone()
        await inter.response.send_message(f"Balance of user - {result}", ephemeral=True)
        await channel.send(f'<@{inter.user.id}> check balance - {result}, for the user - <@{user}>')

    @commands.slash_command(guild_ids=[guild], description='gives a user starcoins')
    @commands.has_permissions(administrator=True)
    async def spay(self, money: int, user:str , inter: disnake.ApplicationCommandInteraction):
        channel = self.bot.get_channel(LogsChannel)
        cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {user}")
        result = cursor.fetchone()
        aye = money + result[0]
        cursor.execute(f"UPDATE main SET balance = '{aye}' WHERE discord_nick='{user}' ")
        connection.commit()
        await inter.response.send_message(f"Balance of user - {aye}", ephemeral=True)
        await channel.send(f'<@{inter.user.id}> check balance - {result}, for the user - <@{user}>')

    @commands.slash_command(guild_ids=[guild], description='takes a certain amount of starcoins')
    @commands.has_permissions(administrator=True)
    async def sdeduct(self, user: str, money: int, inter: disnake.ApplicationCommandInteraction):
        channel = self.bot.get_channel(LogsChannel)
        cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {user}")
        result = cursor.fetchone()
        aye = result[0] - money
        cursor.execute(f"UPDATE main SET balance='{aye}' WHERE discord_nick='{user}'")
        connection.commit()
        await inter.response.send_message(f"you took {aye} starcoins from <@{user}>", ephemeral=True)
        await channel.send(f"<@{inter.user.id}> took {aye} starcoins from <@{user}>")


def setup(bot: commands.Bot):
    bot.add_cog(Staff(bot))