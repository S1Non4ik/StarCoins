import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *


class User(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Main Modules - User is Load')

    @commands.slash_command(guild_ids=[guild], description='displays your balance')
    async def balance(self, inter: disnake.ApplicationCommandInteraction):
        cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {inter.user.name}")
        result = cursor.fetchone()
        if not result is None:
            await inter.response.send_message(f'Your balance - {result[0]}', ephemeral=True)
        else:
            await inter.response.send_message('Error', ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description='pay a user')
    async def pay(self, discord_nick: str, money: int ,inter: disnake.ApplicationCommandInteraction):
        try:
            cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {inter.user.name}")
            result1 = cursor.fetchone()
            aye = result1[0] - money
            if aye != 0:
                cursor.execute(f"SELECT balance FROM main WHERE discord_nick = {discord_nick}")
                result = cursor.fetchone()
                cursor.execute(f"UPDATE main SET balance='{aye}' WHERE discord_nick={inter.user.name}")
                connection.commit()
                all = money + result[0]
                cursor.execute(f"UPDATE main SET balance='{all}' WHERE discord_nick={discord_nick}")
                connection.commit()
                await inter.response.send_message(f'you paid the player - <@{discord_nick}>', ephemeral=True)
            else:
                await inter.response.send_message(f'you dont have enough money', ephemeral=True)
        except Exception as ext:
            print(ext)


def setup(bot: commands.Bot):
    bot.add_cog(User(bot))