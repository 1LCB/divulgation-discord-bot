import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
        print(len(bot.guilds))
    except Exception as e:
        print(e)
    await bot.change_presence(activity=discord.Game(f'custom status'))


@bot.tree.command(name='all-servers', description='send your message to everyone in all servers')
async def div_all(interaction: discord.Interaction, msg: str):
    sent = [interaction.user.id]

    await interaction.response.send_message(f"Sending your message to {len(bot.guilds)} servers...", ephemeral=True)

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
        await interaction.response.send_message(f"Sending your message to {guild.name}...", ephemeral=True)

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
        await interaction.response.send_message("That server couldn't be found!" , ephemeral=True)


@bot.tree.command(name='dm', description="send your message to somemone's dm")
async def dm(interaction: discord.Interaction, msg: str, user_id: str):
    try:
        user = bot.get_user(int(user_id))

        await user.send(msg)
        await interaction.response.send_message(f"✅ Your message was sent to {user.name} ✅", ephemeral=True)
    except:
        await interaction.response.send_message(f"❌ Your message couldn't be sent to that user ❌", ephemeral=True)


@bot.tree.command(name='channel', description="send your message to a specific server's channel")
async def channel(interaction: discord.Interaction, msg: str, channel_id: str):
    try:
        channel_ = bot.get_channel(int(channel_id))

        await channel_.send(msg)
        await interaction.response.send_message(f"✅ Your message was sent to {channel_.name} ✅", ephemeral=True)
    except:
        await interaction.response.send_message(f"❌ Your message couldn't be sent to that channel ❌", ephemeral=True)


bot.run("your bot's token here")