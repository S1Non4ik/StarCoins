import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *

class OnUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print('Event - On_User is Load')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            cursor.execute(f"SELECT discord FROM main WHERE discord = '{member.id}'")
            if not cursor.fetchone() is None:
                pass
            else:
                values = (f"INSERT INTO main (balance,discord_nick ) VALUES(%s, %s)")
                insert = (f'{0}', f'{member.id}')
                cursor.execute(values, insert)
                connection.commit()
        except Exception as ext:
            print(ext)




def setup(bot: commands.Bot):
    bot.add_cog(OnUser(bot))