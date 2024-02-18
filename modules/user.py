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
        cursor.execute(f"SELECT balance FROM main WHERE discord = {inter.user.id}")
        result = cursor.fetchone()
        if not result is None:
            emb = disnake.Embed(title='**Starcoins Bot**',
                                description=f'Your balance - {result[0]}✮',
                                colour=disnake.Colour.gold())
            await inter.response.send_message(embed=emb, ephemeral=True)
        else:
            emb = disnake.Embed(title='📛 Error 📛',
                                description='```Something went wrong```',
                                color=disnake.Color.blurple())
            await inter.response.send_message(embed=emb, ephemeral=True)

    @commands.slash_command(guild_ids=[guild], description='pay a user')
    async def pay(self, discord_nick: str, money: int,inter: disnake.ApplicationCommandInteraction):
        try:
            cursor.execute(f"SELECT balance FROM main WHERE discord = {inter.user.id}")
            result1 = cursor.fetchone()
            aye = result1[0] - money
            if aye != 0:
                discord_nick = discord_nick.replace("<", "").replace("@", "").replace(">", "")
                cursor.execute(f"SELECT balance FROM main WHERE discord = {discord_nick}")
                result = cursor.fetchone()
                cursor.execute(f"UPDATE main SET balance='{aye}' WHERE discord={inter.user.id}")
                connection.commit()
                all = money + result[0]
                cursor.execute(f"UPDATE main SET balance='{all}' WHERE discord={discord_nick}")
                connection.commit()
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'You paid the player - <@{discord_nick}> | Your balance now- {all}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, ephemeral=True)
            else:
                emb = disnake.Embed(title='**Starcoins Bot**',
                                    description=f'You dont have enough money | Your balance now- {result1[0]}✮',
                                    colour=disnake.Colour.gold())
                await inter.response.send_message(embed=emb, ephemeral=True)
        except Exception as ext:
            print(ext)


def setup(bot: commands.Bot):
    bot.add_cog(User(bot))