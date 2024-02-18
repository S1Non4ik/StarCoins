import disnake
import os
from cfg.cfg import *
from disnake.ext import commands
from disnake.ext.commands import Bot

activity = disnake.Streaming(name="With 💙 by S1Non_",url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

intents = disnake.Intents.all()
bot = Bot(command_prefix ='!', intents=intents, activity=activity, status=disnake.Status.do_not_disturb)
bot.remove_command("help")

@bot.event
async def on_ready():
    channel = bot.get_channel(LogsChannel)
    emb = disnake.Embed(title='📚 Start', description='💻 Server answer: ```root@admin:~# Bot is running| ✅```')
    await channel.send(embed=emb)

    async def load_cogg(name):
        bot.load_extension(f"modules.{name}")

    async def reload_cogg(name):
        bot.unload_extension(f"modules.{name}")
        bot.load_extension(f"modules.{name}")


    print('------')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    for filename in os.listdir("./modules"):
        if filename.endswith(".py"):
            try:
                await load_cogg(filename[:-3])
            except Exception as ex:
                print(f"{filename[:-3]} crashed. I'm automaticly fixing it")
                await reload_cogg(filename[:-3])


@bot.slash_command(guild_ids=[guild], description='Restart moduel')
async def restart(inter, name: str):
    if disnake.utils.get(inter.user.roles, id=ModAdmin):
        bot.unload_extension(f"modules.{name}")
        bot.load_extension(f"modules.{name}")
        await inter.response.send_message(f"Moudel - {name} was restared", ephemeral=True)
    else:
        emb = disnake.Embed(title='📛 Error 📛',
                            description='```You dont have enough rights```',
                            color=disnake.Color.blurple())
        await inter.response.send_message(embed=emb)


@bot.slash_command(guild_ids=[guild], description='Stop moduel')
async def stop(inter, name: str):
    if disnake.utils.get(inter.user.roles, id=ModAdmin):
        bot.unload_extension(f"modules.{name}")
        await inter.response.send_message(f"Moudel - {name} was disabled", ephemeral=True)
    else:
        emb = disnake.Embed(title='📛 Error 📛',
                            description='```You dont have enough rights```',
                            color=disnake.Color.blurple())
        await inter.response.send_message(embed=emb)


@bot.slash_command(guild_ids=[guild], description='Run moduel')
async def run(inter, name: str):
    if disnake.utils.get(inter.user.roles, id=ModAdmin):
        bot.load_extension(f"modules.{name}")
        await inter.response.send_message(f"Moudel - {name} has been launched", ephemeral=True)
    else:
        emb = disnake.Embed(title='📛 Error 📛',
                            description='```You dont have enough rights```',
                            color=disnake.Color.blurple())
        await inter.response.send_message(embed=emb)



bot.run(token)