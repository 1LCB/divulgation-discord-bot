import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Game(f'custom status'))

@bot.tree.command(name='all-servers', description='send your message to everyone in all servers')
async def div_all(interaction: discord.Interaction, msg: str):
    sent = [interaction.user.id]

    guilds = bot.guilds
    for g in guilds:
        for m in g.members:
            if m.id in sent:
                continue
            try:
                await m.send(msg)
                sent.append(m.id)
                print(f"[+] Message sent to {m._user}")
            except:
                print(f"[-] Message couldn't be sent to {m._user}")


@bot.tree.command(name='specific-server', description="send your message to everyone in a specific server")
async def specific(interaction: discord.Interaction, msg: str, id_guild: str):
    try:
        guild = bot.get_guild(int(id_guild))
        await interaction.response.send_message(guild.name)

        sent = [interaction.user.id]
        for m in guild.members:
            if m.id in sent:
                continue

            try:
                await m.send(msg)
                sent.append(m.id)
                print(f"[+] Message sent to {m._user}")
            except:
                print(f"[-] Message couldn't be sent to {m._user}")
    except:
        await interaction.response.send_message("This server couldn't be found!")


bot.run("your bot's token here")