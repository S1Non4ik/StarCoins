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
        channel = self.bot.get_channel(NewUserChannel)
        await channel.send(f'Hellow <@{member.id}>')
        try:
            cursor.execute(f"SELECT discord_id FROM main WHERE discord_id = {member.id}")
            if not cursor.fetchone() is None:
                cursor.execute(f"UPDATE main SET discord_nick='{member.name}' WHERE discord_id={member.id}")
                connection.commit()
                pass
            else:
                values = (f"INSERT INTO main (discord_id, balance,discord_nick ) VALUES(%s, %s, %s)")
                insert = (f'{member.id}', f'{0}', f'{member.name}')
                cursor.execute(values, insert)
                connection.commit()
                print('ne v bd')
        except Exception as ext:
            print(ext)




def setup(bot: commands.Bot):
    bot.add_cog(OnUser(bot))