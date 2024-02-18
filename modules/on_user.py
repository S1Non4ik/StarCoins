import disnake
from cfg.cfg import guild
from disnake.ext import commands
from cfg.cfg import *
from dtb.dtb import *
from datetime import date, timedelta

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
                first = (f"INSERT INTO main (balance,discord ) VALUES(%s, %s)")
                FirstInsert = (f'{0}', f'{member.id}')
                cursor.execute(first, FirstInsert)
                connection.commit()
                second = (f"INSERT INTO coin (discord,date) VALUES(%s,%s)")
                SecondInsert = (f'{member.id}', f'{date.today()}')
                cursor.execute(second, SecondInsert)
                connection.commit()
        except Exception as ext:
            print(ext)




def setup(bot: commands.Bot):
    bot.add_cog(OnUser(bot))