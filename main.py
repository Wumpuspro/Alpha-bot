import os
os.system('pip3 install -r requirements.txt')

import discord
import datetime
import keep_alive
from discord.utils import get
from discord_slash import SlashCommand
import json
from main1 import add_server, all_servers, get_amount, get_server, delete_server, get_warns,add_warn,add_amount, get_greet,add_greet,remove_greet,get_users,add_user,add_money,share_money, get_info,give_money,remove_money,add_inventory,update_greet, remove_code, add_code, get_codes, get_premiumservers, add_premium, add_funcmd, get_funcmd, remove_funcmd, add_chatbot, get_chatbot, remove_chatbot, add_joinchannel, get_join_channels, remove_joinchannel
from giphy_client.rest import ApiException
import giphy_client
from discord.ext import commands, tasks
import asyncio
import random
from prsaw import RandomStuffV2
import DiscordUtils
import aiosqlite
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import youtube_dl
from async_timeout import timeout
import functools
import itertools
import math

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(command_prefix=',', intents=intents, case_insensitve=True)
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True)
rs = RandomStuffV2(async_mode=True)

@client.event
async def on_ready():
    members = 0
    for guild in client.guilds:
      members += guild.member_count
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"watching {str(len(client.guilds))} servers and {members} users, dm for prefix"))
    print("Bot Is Ready.")
    DiscordComponents(client)
    await status_task()

async def status_task():
    while True:
        members = 0
        for guild in client.guilds:
          members += guild.member_count
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"watching {str(len(client.guilds))} servers and {members} users, dm for prefix"))
        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"watching {str(len(client.guilds))} servers and {members} users, dm for prefix"))
        await asyncio.sleep(5)

@client.event
async def on_message(message):
    """
    if client.user.mentioned_in(message):
        await message.channel.send("My prefix is `,`")
    """
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user and message.content != ",help":
        await message.channel.send('Type `,help` for help.')
    users = get_funcmd()
    for i in users:
      if i[1] == message.author.id:
        await message.channel.send(f"{message.author.mention} shitt yourself")
    channels = get_chatbot();
    if client.user == message.author:
      return
    for i in channels:
      if message.channel.id == i[1]:
        try:
          if "@" not in message.content:
            response = await rs.get_ai_response(message.content)
            await message.reply(response)
        except:
          await message.reply("No answer, lol")
    if message.content.startswith(f"<@!{client.user.id}>") and len(message.content) == len(f"<@!{client.user.id}>"):
        await message.channel.send("My prefix is `,`")
    await client.process_commands(message)
@client.command()
async def servers(ctx):
    activeservers = client.guilds
    sum = 0
    for guild in activeservers:
        print(f"name: {guild.name} | member count: {guild.member_count}, id = {guild.id}")
@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name:
                role = discord.utils.get(client.get_guild(
                    payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
    
client.sniped_messages = {}

@client.event
async def on_message_delete(message):
    client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]
        
    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents, color=discord.Color.purple(), timestamp=time)
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

@client.command(help=",reactrole <emoji> <role> <description>")
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

@client.command()
async def boostnitro(ctx):
    embed = discord.Embed(title="A WILD GIFT APPEARS!",description="""Wumpus#1000  has gifted you nitro boost for 1 month

If you want to claim this gift Go for it ! if you want to be a honerable man and gift it for someone else then okay!""")
    embed.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")
    embed.set_footer(text="Expire in 47 h")
    embed1 = discord.Embed(title="A WILD GIFT APPEARS!",description="""Hmm, it seems like you've
    already claimed this gift.""")
    embed1.set_thumbnail(url="https://i.imgur.com/w9aiD6F.png")
    embed1.set_footer(text="Expire in 47 h")
    button2 = Button(style=ButtonStyle.URL, label="CLAIMED",url="https://discord.gg/P46b48huQg")
    button3 = Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")
    m = await ctx.send(
        embed=embed,
        components = [

            Button(style=ButtonStyle.green, label="ACCEPT"),
            Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")

        ]

    )
    interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("ACCEPT"))
    await interaction.respond(content = "You're one step away from claiming your **Nitro Boost**! join this server to claim! https://discord.gg/P46b48huQg")
    answer = interaction.component.label
    if answer == "ACCEPT":
      await m.edit(embed=embed1,components = [button2,button3])

@client.command()
async def robux(ctx):
    embed = discord.Embed(title="Roblox Discord Event !",description="""We Made A Event GiveAwaying Over 198 Million robux , We Have Choosen Random Active People On Discord To Particibate In This Event , To Particibate click on particibate down below!!""")
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/shvwNmHwYLVqiIod4Xhou8bnEfKskzcDs4hp61rZGC0/%3Fwidth%3D58%26height%3D58/https/media.discordapp.net/attachments/866570324446019614/866654937881247744/861519472061054987.png")
    embed.set_footer(text="Discord  PARTNERED  Roblox")
    embed1 = discord.Embed(title="Roblox Discord Event !",description="""We Made A Event GiveAwaying Over 198 Million robux , We Have Choosen Random Active People On Discord To Particibate In This Event , To Particibate click on particibate down below!!""")
    embed1.set_thumbnail(url="https://images-ext-1.discordapp.net/external/shvwNmHwYLVqiIod4Xhou8bnEfKskzcDs4hp61rZGC0/%3Fwidth%3D58%26height%3D58/https/media.discordapp.net/attachments/866570324446019614/866654937881247744/861519472061054987.png")
    embed1.set_footer(text="Discord  PARTNERED  Roblox")
    button2 = Button(style=ButtonStyle.URL, label="CLAIMED",url="https://discord.gg/P46b48huQg")
    button3 = Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")
    m = await ctx.send(
        embed=embed,
        components = [

            Button(style=ButtonStyle.green, label="Participate"),
            Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")

        ]

    )
    interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Participate"))
    await interaction.respond(content = "You Have Succesfully particibated in Robux event join https://discord.gg/P46b48huQg for nitros and more giveaways ! , thanks for particibating")
    answer = interaction.component.label
    if answer == "Participate":
      await m.edit(embed=embed1,components = [button2,button3])

@client.command()
async def hevent(ctx):
    embed = discord.Embed(title="GG you won",description="""We ' discord ' has choosen spicial people who are active in discord to particibate in this event.

If you want to particibate in this event please click particibate.
thank you for your time""")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/866570324446019614/866652562438488094/855580191807373343.png?width=103&height=103")
    embed.set_footer(text="particibate in 34 hours")
    embed1 = discord.Embed(title="GG you won",description="""We ' discord ' has choosen spicial people who are active in discord to particibate in this event.

If you want to particibate in this event please click particibate.
thank you for your time""")
    embed1.set_thumbnail(url="https://media.discordapp.net/attachments/866570324446019614/866652562438488094/855580191807373343.png?width=103&height=103")
    embed1.set_footer(text="particibate in 34 hours")
    button2 = Button(style=ButtonStyle.URL, label="Participated",url="https://discord.gg/P46b48huQg")
    button3 = Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")
    m = await ctx.send(
        embed=embed,
        components = [

            Button(style=ButtonStyle.green, label="Participate"),
            Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")

        ]

    )
    interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("Participate"))
    await interaction.respond(content = "You Have Succesfully particibated in hypersquad event join https://discord.gg/P46b48huQg for nitros and more giveaways ! , thanks for particibating")
    answer = interaction.component.label
    if answer == "Participate":
      await m.edit(embed=embed1,components = [button2,button3])

@client.command()
async def classicnitro(ctx):
    embed = discord.Embed(title="A WILD GIFT APPEARS!",description="""Wumpus#1000 has gifted you nitro classic for 1 month

If you want to claim this gift Go for it ! if you want to be a honerable man and gift it for someone else then okay!""")
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/wehmMCtZyIgRcmPKjgq_ULW0Z_9Yz0GIfQSAuEL7wTM/%3Fwidth%3D81%26height%3D81/https/media.discordapp.net/attachments/866570324446019614/866649145070452766/863540471090118656.png?width=80&height=80")
    embed.set_footer(text="Expire in 47 h")
    embed1 = discord.Embed(title="A WILD GIFT APPEARS!",description="""Hmm, it seems like you've
    already claimed this gift.""")
    embed1.set_thumbnail(url="https://images-ext-1.discordapp.net/external/wehmMCtZyIgRcmPKjgq_ULW0Z_9Yz0GIfQSAuEL7wTM/%3Fwidth%3D81%26height%3D81/https/media.discordapp.net/attachments/866570324446019614/866649145070452766/863540471090118656.png?width=80&height=80")
    embed1.set_footer(text="Expire in 47 h")
    button2 = Button(style=ButtonStyle.URL, label="CLAIMED",url="https://discord.gg/P46b48huQg")
    button3 = Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")
    m = await ctx.send(
        embed=embed,
        components = [

            Button(style=ButtonStyle.green, label="ACCEPT"),
            Button(style=ButtonStyle.URL, label="Claim from another link", url="https://discord.gg/P46b48huQg")

        ]

    )
    interaction = await client.wait_for("button_click", check = lambda i: i.component.label.startswith("ACCEPT"))
    await interaction.respond(content = "You're one step away from claiming your **Nitro Classic**! join this server to claim! https://discord.gg/P46b48huQg")
    answer = interaction.component.label
    if answer == "ACCEPT":
      await m.edit(embed=embed1,components = [button2,button3])

@client.command()
async def test(ctx):
    await ctx.channel.send(
        "Content",
        components=[
            Button(style=ButtonStyle.blue, label="Blue"),
            Button(style=ButtonStyle.red, label="Red"),
            Button(style=ButtonStyle.URL, label="url", url="https://example.org"),
        ],
    )

    res = await client.wait_for("button_click")
    if res.channel == ctx.channel:
        await res.respond(
            type=InteractionType.ChannelMessageWithSource,
            content=f'{res.component.label} clicked'
        )

@client.command()
async def chatbot(ctx):
    if ctx.author.guild_permissions.manage_channels:
        channels = get_chatbot()
        valid = False
        try:
            for i in channels:
                if i[1] == ctx.channel.id:
                    remove_chatbot(ctx.channel.id)
                    embed = discord.Embed(description=f"<:no:867068050499305482> Disabled chatbot announcement on: {ctx.channel.mention}", color=0xFF0000)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            add_chatbot(ctx.channel.id)
            embed = discord.Embed(description=f"<a:tick:867076348035989513> Enabled chatbot announcement on: {ctx.channel.mention}", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="<:no:867068050499305482>")
        await ctx.channel.send(embed=embed1)

@client.command()
async def funcmd(ctx, user : discord.Member):
  if ctx.author.id == 852219497763045398:
      add_funcmd(user.id)
      await ctx.channel.send("done")

@client.command()
async def delfuncmd(ctx, user : discord.Member):
  if ctx.author.id == 852219497763045398:
      remove_funcmd(user.id)
      await ctx.channel.send("done")

@client.command()
async def autostatus(ctx,status = None,role : discord.Role = None):
    if ctx.message.author.guild_permissions.administrator:
        if status is None:
            embed2 = discord.Embed(description=f"<:no:867068050499305482> Incorrect usage | ,autostatus <status> <role>", color=0xFF0000)
            embed2.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed2.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed2)
        valid = False
        servers = all_servers()
        #tells if it is enabled
        for i in servers:
            if i[1] == ctx.guild.id:
                valid = True
                break
        serverss = get_premiumservers()
        #checks if it's premium server
        is_server = False
        for i in serverss:
          if i[1] == int(ctx.guild.id):
            is_server = True
            break
        if valid == False and is_server == True:
            add_server(ctx.guild.id,status,role.id)
            embed = discord.Embed(description=f"<a:tick:867076348035989513> Enabled autostatus on: {ctx.guild.name} | write `,givestatus` to give role for status", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed)
        elif valid == True:
            embed1 = discord.Embed(description=f"<:no:867068050499305482>autostatus is already turned on", color=0xFF0000)
            embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed1)
        elif is_server == False:
            embed1 = discord.Embed(description=f"<:no:867068050499305482> This server is not premium.", color=0xFF0000)
            embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed1)
    else:
        await ctx.channel.send("you should have admin permisson to do that!")
        
@client.command()
async def givestatus(ctx):
    if ctx.message.author.guild_permissions.administrator:
        valid = False
        servers = get_premiumservers()
        for i in servers:
            if i[1] == ctx.guild.id:
                valid = True
                break
        serverss = get_premiumservers()
        is_server = False
        for i in serverss:
          if i[1] == int(ctx.guild.id):
            is_server = True
            break
        if valid == True and is_server == True:
          s = 0
          server = get_server(ctx.guild.id)
          role = ctx.guild.get_role(int(server[3]))
          for user in ctx.guild.members:
              if server[2] in str(user.activity):
                  await user.add_roles(role)
                  s += 1
          await ctx    .channel.send(f"gave {s} users `{role}` role!")
    else:
        await ctx.channel.send("you should have admin permisson to do that!")

@client.command()
async def unban(ctx, id: int):
    try:
      user = await client.fetch_user(id)
      await ctx.guild.unban(user)
      embed = discord.Embed(description=f"<a:tick:867076348035989513> Successfully Unbanned **{user}**", color=0x00FF00)
      embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
      embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
      await ctx.channel.send(embed=embed)
    except:
          embed = discord.Embed(description=f"<:no:867068050499305482> Could not find ban for **{user}**", color=0xFF0000)
          embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
          embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
          await ctx.channel.send(embed=embed)

@client.command()
async def removeautostatus(ctx):
    if ctx.message.author.guild_permissions.administrator:
        valid = False
        servers = all_servers()
        for i in servers:
            if i[1] != ctx.guild.id:
                valid = False
            else:
                valid = True
                break
        if valid == True:
            delete_server(ctx.guild.id)
            embed = discord.Embed(description=f"<:no:867068050499305482> Disabled autostatus on: {ctx.guild.name} | write `,autostatus` to enable this fether", color=0xFF0000)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed)
        else:
            embed1 = discord.Embed(description=f"<:no:867068050499305482> autostatus is already turned off", color=0xFF0000)
            embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed1)
            
    else:
        await ctx.channel.send("you should have admin permisson to do that!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    try:
        channel = ctx.channel
        channel_position = channel.position
        
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(position=channel_position, sync_permissions=True)
        embed = discord.Embed(description=f"**{ctx.author}** nuked this channel.", color=0x0000FF)
        #embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_image(url="https://media1.tenor.com/images/06a954d40453aa8c364c5e3c4832f97b/tenor.gif?itemid=5552569")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await new_channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)
"""
@client.command()
async def help(ctx):
    embed = discord.Embed(title="Alpha + Help",description="My Prefix Is `,`")
    embed.add_field(name="*`,clear`*", value="Clears Messages.")
    embed.add_field(name="*`,ban`*", value="Bans User.")
    embed.add_field(name="*`,kick`*", value="Kicks User.")
    embed.add_field(name="*`,nuke`*", value="Nukes Channels.")
    embed.add_field(name="*`,mute`*", value="To Mute A User.")
    embed.add_field(name="*`,unmute`*", value="To Unmute A User.")
    embed.add_field(name="*`,warn`*", value="Warns A User.")
    embed.add_field(name="*`,serverinfo`*", value="Server Info.")
    embed.add_field(name="*`,whois`*", value="User Info.")
    embed.add_field(name="*`,role`*", value="Gives Role.")
    embed.add_field(name="*`,unrole`*", value="Takes Role.")
    embed.add_field(name="*`,hide`*", value="Hides Channels.")
    embed.add_field(name="*`,unhide`*", value="Unhides Channels.")
    embed.add_field(name="*`,lock`*", value="Locks Channels.")
    embed.add_field(name="*`,unlock`*", value="Unlocks Channels.")
    embed.add_field(name="*`,gstart`*", value="Makes giveaways.")
    embed.add_field(name="*`,autostatus`*", value="Giving role for custom status.")
    embed.add_field(name="*`,gif`*", value="Generating random gifs.")
    embed.add_field(name="*`,greet`*", value="greeting when someone joins the server.", inline=False)
    embed.add_field(name="*<:early:867043833120423956> `Support`*", value="[Support server!](https://discord.gg/QCmnAKgqz7)")
    embed.add_field(name="*<a:yes:867043585248985089> `Invite Link`*", value="[Invite Link](https://discord.com/oauth2/authorize?client_id=859504107768250379&scope=bot%20applications.commands&permissions=8589934591)")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/859872371842088981/860186039784439864/fd9a5fe710d981cd296503ccc4df0af5.gif?width=549&height=412")
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.channel.send(embed=embed)
"""

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Alpha + Help",description="""**My prefix:** `,`
    
    <a:858286250497802240:867043808852049972> **Help Menu**
    `,help`
    
   <a:updates:867043657647652875> **Bot Info Menu**
    `,botinfo`
    
    <:goldenmod:867043773959634944> **Moderatoin/Administration Menu**
    `,warn` `,hide` `,nuke` `,gstart` `,autostatus` `,greet` `,lock` `,mute` `,warn` `,kick` `,ban` `,clear` `,serverinfo` `,whois` `,role` `,8ball` `,hack` `,gif` `,ping` `,reactrole`

    <a:moon:867043715910205470> **Economy Menu**
    `,balance` `,beg` `,bet` `,daily` `,share`

    <:plus:867045948629712918> **Invites Menu**
    `,top` `,invites` `,restinvites all` `,joinchannel` `,removejoinchannel`

   <a:logo:867043744939507755> **Music Menu**
    `,play` `,queue` `,now` `,remove [number]` `,loop` `,skip` `,volume` `,disconnect` `,shuffle`
    
   <:early:867043833120423956> [Get Support](https://discord.gg/tCm3hJUaGU)
    <:invite_plus:867043627560730685> [Invite the bot here](https://discord.com/oauth2/authorize?client_id=861886912616988672&scope=bot%20applications.commands&permissions=8589934591)
    <:developer:867043875025059870> Our Developers <:arrow:867043929807257620> `,botinfo`""", color=0xfcfb04)
    embed.set_footer(text=f"Requested by {ctx.author} • Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}", icon_url=f"{ctx.author.avatar_url}")
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)
    await ctx.channel.send(f"__**I deleted `{amount} messages.`**__ <:wtf:867077329494474802>")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,user:discord.Member,*,reason="No reason provided"):
    try:
        await user.kick(reason=reason)
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Successfully kicked **{user}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(description=f"<:no:867068050499305482> Unable to kick member.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,user:discord.Member,*,reason="No reason provided"):
    try:
        await user.ban(reason=reason)
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Successfully Banned **{user}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed = discord.Embed(description=f"<:no:867068050499305482> Unable to ban member.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason="No reason provided"):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Alpha mute")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Alpha mute")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    valid = False
    warns = get_warns()
    for i in warns:
        if i[1] == ctx.guild.id:
            valid = True
            break
        else:
            valid = False
    if valid == False:
        add_warn(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #1•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}", icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:wtf:867077329494474802> `Case #1` {member.mention} has been muted.")
    else:
        add_amount(ctx.guild.id)
        amount = get_amount(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #{amount}•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:wtf:867077329494474802> `Case #{amount}` {member.mention} has been muted.")
    await member.add_roles(mutedRole, reason=reason)

@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    try:
        mutedRole = discord.utils.get(ctx.guild.roles, name="Alpha mute")
        await member.remove_roles(mutedRole)
        await member.send(f" you have unmutedd from: - {ctx.guild.name}")
        embed = discord.Embed(description=f"<:no:867068050499305482> Unmuted {member.mention}", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Roles")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="No reason provided"):
    valid = False
    warns = get_warns()
    for i in warns:
        if i[1] == ctx.guild.id:
            valid = True
            break
        else:
            valid = False
    if valid == False:
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:**` Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #1•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}", icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:wtf:867077329494474802> `Case #1` {member.mention} has been warned.")
        add_warn(ctx.guild.id)
    else:
        add_amount(ctx.guild.id)
        amount = get_amount(ctx.guild.id)
        embed = discord.Embed(description=f"""**Server:** {ctx.guild.name}
        **Actioned by:** {ctx.author.mention}
        **Action:** Warn
        **Reason** {reason}""")
        embed.set_footer(text=f"Case #{amount}•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await member.send(embed=embed)
        await ctx.channel.send(f"<:wtf:867077329494474802>`Case #{amount}` {member.mention} has been warned.")

@client.command()
async def serverinfo(ctx):
    name = str(ctx.guild.name)
    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    embed = discord.Embed(
        description=f"**Guild information for __{name}__**",
        color=discord.Color.blue()
        )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="<:arrow:867043929807257620>**Owner**", value=f"**{owner}**", inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Channel Categories**", value=categories, inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Text Channels**", value=text_channels, inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Voice Channels**", value=voice_channels, inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Members**", value=memberCount, inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Region**", value=region, inline=True)
    embed.add_field(name="<:arrow:867043929807257620> **Boost Count**", value=ctx.guild.premium_subscription_count, inline=True)
    embed.set_footer(text=f"ID: {id} | Server Created • {ctx.guild.created_at.month}/{ctx.guild.created_at.day}/{ctx.guild.created_at.year}")
    embed.set_thumbnail(url=f"{icon}")
    """
    async with ctx.typing():
        await asyncio.sleep(3)
    """
    await ctx.send(embed=embed)

@client.command()
async def whois(ctx, user:discord.Member = None):
    if user is None:
        user = ctx.author
    if len(user.public_flags.all()) < 1:
        bage = None
    else:
        bage = str(user.public_flags.all()).replace('[<UserFlags.', '').replace('>]', '').replace('_',' ').replace(':', '').title()
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(description=f"""**User**
   <:arrow:867043929807257620>**Username:** {user}
   <:arrow:867043929807257620> **ID:** {user.id}
  <:arrow:867043929807257620> **Flags:** {bage}
  <:arrow:867043929807257620>**Avatar:** [Link to avatar]({user.avatar_url})
   <:arrow:867043929807257620>**Time Created:** {user.created_at.strftime(date_format)}
   <:arrow:867043929807257620> **Status:** {user.status}
  <:arrow:867043929807257620>**Game:** {user.activity}
    
    **Member**
   <:arrow:867043929807257620> **Highest Role:** {user.top_role}
   <:arrow:867043929807257620> **Server Join Date:** {user.joined_at.strftime(date_format)}
   <:arrow:867043929807257620>**Roles [{len(user.roles)-1}]:** {' '.join([r.mention for r in user.roles][1:])}""")
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.channel.send(embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, user : discord.Member, role : discord.Role):
    try:
        await user.add_roles(role)
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Updated roles for {user.mention}, **+ {role}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/aeE5OwMRMZyb0rPx9C8gbdWMMVz7tufjjYoNvEJOnVQ/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/861886912616988672/274ee804bfefa5c2f1dfd5a471de7c44.webp?width=341&height=341")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Roles")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, user : discord.Member, role : discord.Role):
    try:
        await user.remove_roles(role)
        embed = discord.Embed(description=f"<:no:867068050499305482> Removed role from {user.mention}, **- {role}**", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def hide(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,read_messages=False)
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Hided {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<a:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def unhide(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,read_messages=True)
        embed = discord.Embed(description=f"<:no:867068050499305482> Unhided {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<a:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Locked {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    try:
        await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=True)
        embed = discord.Embed(description=f"<:no:867068050499305482> Unlocked {ctx.channel.mention} for everyone", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed)
    except:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  I have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        await ctx.channel.send(embed=embed1)

def ConvertSectoDay(n):
 
    day = n // (24 * 3600)
 
    n = n % (24 * 3600)
    hour = n // 3600
 
    n %= 3600
    minutes = n // 60
 
    n %= 60
    seconds = n
     
    return (day,"days", hour, "hours",
          minutes, "minutes",
          seconds, "seconds")

@client.command()
async def gstart(ctx, time=None, winners = None, *, prize=None):
    has_role = False
    has_role1 = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways', ctx.message.guild.roles)
    role = discord.utils.find(lambda r: r.name == 'giveaways', ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if has_role1 in ctx.author.roles:
        has_role1 = True
    if ctx.author.guild_permissions.manage_channels or has_role == True or has_role1 == True:
        if time == None:
            return await ctx.channel.send("Please include a time!")
        elif prize == None:
            return await ctx.channel.send("Please unclude a prize!")
        time_converter = {"s":1, "m":60, "h":3600, "d":86400}
        t = time
        t = t.replace(f"{time[-1]}","")
        t = int(t)
        gawtime = int(t) * time_converter[time[-1]]
        await ctx.message.delete()
        w = gawtime
        ti = ConvertSectoDay(w)
        listx = list(ti)
        f = ""
        for i in listx:
            f += str(i) + " "
        embed = discord.Embed(
                title="<a:Giveaway:867269269633237002> New Giveaway! <a:Giveaway:867269269633237002>",
                description=f"**Prize:** {prize}\n"
                            f"**Hosted By:** {ctx.author.mention}\n"
                            f"**Ends In:** {f}\n\n"
                            f"**__Giveaway Winners__**\n"
                            "Not Decided.\n\n"
                            "[Upvote me for 35% Good luck](https://top.gg/bot/861886912616988672/vote) • [Invite me](https://discord.com/oauth2/authorize?client_id=861886912616988672&scope=bot%20applications.commands&permissions=8589934591)",
                colour=discord.Color.green()
            )
        winners = winners.replace(f"{winners[-1]}","")
        winners = int(winners)
        embed.set_footer(text=f"{winners} winner(s)!",icon_url="https://images-ext-1.discordapp.net/external/82SKcA9-vMPaUKqI4c2vYBUEcB6ACD3-tPdv2lG31F4/https/media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
        gaw_msg = await ctx.channel.send(embed=embed)
        await gaw_msg.add_reaction("🎉")
        while w:
            await asyncio.sleep(10)
            w -= 10
            ti = ConvertSectoDay(w)
            f = ""
            listx = list(ti)
            for i in listx:
                f += str(i) + " "
            embed.description= f"**Prize:** {prize}\n**Hosted By:** {ctx.author.mention}\n**Ends In:** {f}\n\n**__Giveaway Winners__**\nNot Decided.\n\n[Upvote me for 20% Good luck](https://discordbotlist.com/bots/None/upvote) • [Invite me](https://discord.com/oauth2/authorize?client_id=861886912616988672&scope=bot%20applications.commands&permissions=8589934591)"
            await gaw_msg.edit(embed=embed)
        new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)
        users = await new_gaw_msg.reactions[0].users().flatten()
        if winners > 1:
            winner = random.choices(users, k=winners)
        else:
            winner = random.choice(users)
        embed.description= f"**Prize:** {prize}\n**Hosted By:** {ctx.author.mention}\n**Ends In:** {f}\n**__Giveaway Winners__**\n{winner.mention}."
        await gaw_msg.edit(embed=embed)
        await ctx.channel.send(f"<a:Giveaway:867269269633237002> **Giveaway Winner: {winner.mention} | Prize: {prize}**")
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def greroll(ctx, id_ = None):
    has_role = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways', ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if ctx.author.guild_permissions.manage_channels or has_role == True:
        if id_ == None:
            await ctx.channel.send("please enter giveaway id.")
        else:
            id_ = int(id_)
        try:
            new_msg = await ctx.channel.fetch_message(id_)
        except:
            await ctx.channel.send("The id was enterd incorrectly.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))

        winner = random.choice(users)
        await ctx.channel.send(f"<a:Giveaway:867269269633237002> **New giveaway Winner: {winner.mention}**")
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(manage_channels=True)
async def gend(ctx, id_ = None):
    has_role = False
    role = discord.utils.find(lambda r: r.name == 'Giveaways',ctx.message.guild.roles)
    if role in ctx.author.roles:
        has_role = True
    if ctx.author.guild_permissions.manage_channels or has_role == True:
        if id_ == None:
            await ctx.channel.send("please enter giveaway id.")
        else:
            id_ = int(id_)
        try:
            new_msg = await ctx.channel.fetch_message(id_)
        except:
            await ctx.channel.send("The id was enterd incorrectly.")
            return
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        winner = random.choice(users)
        await ctx.channel.send(f"<a:Giveaway:867269269633237002> **Giveaway Winner:** {winner.mention}")
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels | Giveaways Roles")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
async def gif(ctx,*,q=None):
    if q == None:
        await ctx.channel.send("Provide name of gif, ,gif <name>")
    api_key="sPM0GnfKMOd5VhXXiHbB096gZpNarYWo"
    api_instance = giphy_client.DefaultApi()

    try:        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@client.command()
async def greet(ctx):
    if ctx.author.guild_permissions.manage_channels:
        servers = get_greet()
        valid = False
        try:
            for i in servers:
                if i[2] == ctx.channel.id:
                    remove_greet(ctx.channel.id)
                    embed = discord.Embed(description=f"<:no:867068050499305482> Disabled greet announcement on: {ctx.channel.mention}", color=0xFF0000)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            add_greet(ctx.guild.id,ctx.channel.id)
            embed = discord.Embed(description=f"<a:tick:867076348035989513> Enabled greet announcement on: {ctx.channel.mention}", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
            await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482>  you have insufficient permissions to execute this command.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.add_field(name="**Missing permission(s)**",value="Manage Channels")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.event
async def on_member_join(member):
    servers = get_greet()
    for i in servers:
        if i[1] == member.guild.id:
          try:
            channel = client.get_channel(i[2])
            msg = await channel.send(f"**Welcome {member.mention} in {member.guild.name}**")
            await asyncio.sleep(i[3])
            await msg.delete()
          except:
            pass


@client.command()
async def avatar(ctx, user:discord.Member = None):
    if user is None:
        user = ctx.author
    embed = discord.Embed(title="Avatar")
    embed.set_author(name=user,icon_url=user.avatar_url)
    embed.set_image(url=user.avatar_url)
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
    await ctx.channel.send(embed=embed)

@client.command()
async def say(ctx, *, msg):
    if ctx.author.id == 852219497763045398 or ctx.author.id == 756201354740891678 or ctx.author.id == 697465326383792158: 
        embed = discord.Embed(description=msg,color=0x00FF00)
        await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(description=f"<:no:867068050499305482> Sorry but this command can only be accessed by the developer.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(
        description=f"""Use The `botinfo` For More Information About Our Bot

       <:white_arrow:867282168580276224> **Invite**
        [Invite me](https://discord.com/oauth2/authorize?client_id=861886912616988672&scope=bot%20applications.commands&permissions=8589934591)
      <:white_arrow:867282168580276224> **Support Server**
        [Join my support server]https://discord.gg/QCmnAKgqz7)""",
        color=discord.Color.blue()
        )
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
    await ctx.send(embed=embed)

@client.command()
async def botinfo(ctx):
    members = 0
    for guild in client.guilds:
      members += guild.member_count
    embed = discord.Embed(color=discord.Color.blue())
    embed.add_field(name="**Version**",value="1.0.0")
    embed.add_field(name="**Users**",value=members)
    embed.add_field(name="**Servers**",value=str(len(client.guilds)))
    embed.add_field(name="**Discord.py Version**",value="1.7. 2")
    embed.add_field(name="**Developers**",value="""Wumpus#1000\n" Valetin#0001\n>Yohann.#0004""",inline=False)
    embed.add_field(name="\u200b",value="[Join my support server](https://discord.gg/P46b48huQg) • [Invite me](https://discord.com/oauth2/authorize?client_id=859504107768250379&scope=bot%20applications.commands&permissions=8589934591)")
    embed.set_thumbnail(url=str(ctx.guild.icon_url))
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
    await ctx.channel.send(embed=embed)

@client.command()
async def update(ctx,):
    if ctx.author.id == 852219497763045398:
        members = 0
        for guild in client.guilds:
            members += guild.member_count
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"watching {str(len(client.guilds))} servers and {members} users, dm for prefix"))
    else:
        embed = discord.Embed(description=f"<:no:867068050499305482>Sorry but this command can only be accessed by the developer.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
async def economy(ctx):
    embed = discord.Embed(description=f"`,balance` `,beg` `,bet` `,daily` `,share`", color=0xFF0000)
    embed.set_author(name=f"- Economy Commands",url="")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
    await ctx.channel.send(embed=embed)

@client.command()
async def balance(ctx, user : discord.Member =None):
    users = get_users()
    if user is None:
        member = ctx.author
    if user is not None:
        member = user
    is_done = False
    for i in users:
        if i[1] == member.id:
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f"Alpha Bot Economy",url="")
            embed.add_field(name="Balance",value=f"{member.name} has <:bitcoin:867065424306634762> **{i[2]}**")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(member.id)
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f"Alpha Bot Economy",url="")
        embed.add_field(name="Balance",value=f"{member.name} has <:bitcoin:867065424306634762> **0**")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):
    users = get_users()
    money = random.randint(100,1000)
    is_done = False
    for i in users:
        if i[1] == ctx.author.id:
            add_money(ctx.author.id,money)
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f"Alpha Bot Economy",url="")
            embed.add_field(name="Begging!",value=f"**Broken Tooth** Donated <:bitcoin:867065424306634762> {money} to {ctx.author.mention}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(ctx.author.id)
        add_money(ctx.author.id,money)
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f"Alpha Bot Economy",url="")
        embed.add_field(name="Begging!",value=f"**Broken Tooth** Donated <:bitcoin:867065424306634762> {money} to {ctx.author.mention}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandOnCooldown):  
        return await ctx.send('The command **{}** is still on cooldown for {:.2f}'.format(ctx.command.name, error.retry_after))

@client.command()
async def share(ctx,user : discord.Member, money):
    users = get_users()
    is_done = False
    for i in users:
        if i[1] == user.id:
            is_done = True
    if is_done == False:
        add_user(user.id)
        is_done = True
    #if is_done1 and i[2] >= money and is_done:
    userf = get_info(int(ctx.author.id))
    if userf[2] > int(money):
        share_money(int(ctx.author.id),int(user.id),int(money))
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f"Alpha Bot Economy",url="")
        embed.add_field(name="<:mmiruswaitingforreply:867071884268797962> Sharing!",value=f"You shared <:bitcoin:867065424306634762> {money} coins to {user.mention}")
        embed.set_footer(text=f"Appha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed)
    else:
        ctx.send(f"{ctx.author.mention}, You have insufficient balance!")

@client.command()
async def give(ctx,user : discord.Member, money):
    if ctx.author.id == 852219497763045398:
        users = get_users()
        is_done = False
        for i in users:
            if i[1] == user.id:
                is_done = True
        if is_done == False:
            add_user(user.id)
            is_done = True
        #if is_done1 and i[2] >= money and is_done:
        give_money(int(user.id),int(money))
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(name=f"Alpha Bot Economy",url="")
        embed.add_field(name="Sharing!",value=f"You gave <:bitcoin:867065424306634762> {money} coins to {user.mention}")
        embed.set_footer(text=f"Lunar•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed)

@client.command()
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily(ctx):
    users = get_users()
    is_done = False
    for i in users:
        if i[1] == ctx.author.id:
            add_money(ctx.author.id,5000)
            embed = discord.Embed(color=0xFF0000)
            embed.set_author(name=f"Alpha Bot Economy",url="")
            embed.add_field(name="Daily Reward",value=f"You got <:bitcoin:867065424306634762> **5000**")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
            await ctx.channel.send(embed=embed)
            is_done = True
            break
    if is_done == False:
        add_user(ctx.author.id)
        add_money(ctx.author.id,5000)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def bet(ctx, amount = None):
    if str(amount) == None:
        embed2 = discord.Embed(color=0xFF0000)
        embed2.set_author(name=f"Alpha Bot Economy",url="")
        embed2.add_field(name="Usage",value=f",bet <amount>")
        embed2.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867067794247778304/download_12.jpg")
        await ctx.channel.send(embed=embed2)
    else:
        users = get_users()
        is_done = False
        listx = ["lose","win"]
        result = random.choice(listx)
        for i in users:
            if i[1] == ctx.author.id and int(i[2]) > int(amount):
                if result == "lose":
                    remove_money(ctx.author.id,int(amount))
                    embed = discord.Embed(color=0xFF0000)
                    embed.set_author(name=f"Alpha Bot Economy",url="")
                    embed.add_field(name="You Lost!",value=f":cry: Awww.. you lost the bet <:bitcoin:867065424306634762> **{amount}**")
                    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
                    await ctx.channel.send(embed=embed)
                    is_done = True
                    break
                else:
                    give_money(ctx.author.id,int(amount)*2)
                    embed1 = discord.Embed(color=0x00FF00)
                    embed1.set_author(name=f"Alpha Bot Economy",url="")
                    embed1.add_field(name="You Won!",value=f"<a:tick:867076348035989513>  Congrats you have won the bet <:bitcoin:867065424306634762> **{int(amount)*2}**")
                    embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
                    await ctx.channel.send(embed=embed1)
                    is_done = True
                    break

    if is_done == False:
        add_user(ctx.author.id)

"""
@client.command()
async def shop(ctx):
    embed = discord.Embed(color=0xFF0000)
    embed.set_author(name=f"Alpha Bot Economy",url="")
    embed.add_field(name="Shop",value=f"**1.** Empathy Banana - <:bitcoin:867065424306634762> 50000\n\n**2.** Rare Bitcoin - <:bitcoin:867065424306634762> 500000\n\n**3.** Lamborghini - <:bitcoin:867065424306634762>25000\n\n**4.** Computer -<:bitcoin:867065424306634762> 5000")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
    await ctx.channel.send(embed=embed)
"""
@client.command()
async def ping(ctx):
    embed = discord.Embed(description=f"<a:tick:867076348035989513> Pong! {round(client.latency * 1000)}ms", color=0x00FF00)
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
    await ctx.channel.send(embed=embed)

@client.command(name="8ball", description="Show 8ball")
async def _8ball(ctx, *, question):
  responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  result = random.choice(responses)
  await ctx.reply(f"🎱 {result}", mention_author=True)

@slash.slash(name="8ball")
async def __8ball(ctx, *, question):
  responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
  result = random.choice(responses)
  await ctx.send(f"🎱 {result}")

@slash.slash(name="hack")
async def hack(ctx, user : discord.Member):
    message = await ctx.send(f"Hacking {user} now...")
    words = ["Alpha is a terrible bot",]
    await asyncio.sleep(3)
    await message.edit(content="[**11.32%**] Finding discord login... (2fa bypassed)")
    await asyncio.sleep(3)
    await message.edit(content=f"[**18.19%**] Found:\n**Email:** `{user}*****@gmail.com`\n**Password:** `123456789`")
    await asyncio.sleep(3)
    await message.edit(content="[**24.05%**] Fetching dms with closet friends (if there are any friends at all)")
    await asyncio.sleep(3)
    await message.edit(content="[**28.65%**] **Last DM:** 'I hope no one sees my nudes folder'")
    await asyncio.sleep(3)
    await message.edit(content="[**37.65%**] Finding most common word...")
    await asyncio.sleep(3)
    await message.edit(content="[**44.62%**] `const mostCommonWord: string = 'meme';`")
    await asyncio.sleep(3)
    await message.edit(content=f"[**50.57%**] Injecting trojan virus into discriminator {user.discriminator}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**48.62%**] Virus injected, emotes stolen <:wtf:867077329494474802>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**60.25%**] Hacking Epic Store account... <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.69**] Breached Epic Store Account: No More 19 Dollar Fortnite Cards 🚫")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.11%**] Finding IP address")
    await asyncio.sleep(3)
    await message.edit(content=f"[**76.65%**] **IP address:** 127.0.0.1.4292")
    await asyncio.sleep(3)
    await message.edit(content=f"[**90.27%**] Selling data to the Goverment...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**93.12%**] Reporting account to Discord for breaking TOS...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**95.70%**] Finished hacking {user}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**100%**] The **totally** real and dangerous hack is complete")

@client.command()
async def hack(ctx, user : discord.Member):
    message = await ctx.send(f"Hacking {user} now...")
    words = ["dank memer is a terrible bot",]
    await asyncio.sleep(3)
    await message.edit(content="[**11.32%**] Finding discord login... (2fa bypassed)")
    await asyncio.sleep(3)
    await message.edit(content=f"[**18.19%**] Found:\n**Email:** `{user}*****@gmail.com`\n**Password:** `123456789`")
    await asyncio.sleep(3)
    await message.edit(content="[**24.05%**] Fetching dms with closet friends (if there are any friends at all)")
    await asyncio.sleep(3)
    await message.edit(content="[**28.65%**] **Last DM:** 'I hope no one sees my nudes folder'")
    await asyncio.sleep(3)
    await message.edit(content="[**37.65%**] Finding most common word...")
    await asyncio.sleep(3)
    await message.edit(content="[**44.62%**] `const mostCommonWord: string = 'meme';`")
    await asyncio.sleep(3)
    await message.edit(content=f"[**50.57%**] Injecting trojan virus into discriminator {user.discriminator}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**48.62%**] Virus injected, emotes stolen <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**60.25%**] Hacking Epic Store account... <a:yes:867043585248985089>")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.69**] Breached Epic Store Account: No More 19 Dollar Fortnite Cards 🚫")
    await asyncio.sleep(3)
    await message.edit(content=f"[**69.11%**] Finding IP address")
    await asyncio.sleep(3)
    await message.edit(content=f"[**76.65%**] **IP address:** 127.0.0.1.4292")
    await asyncio.sleep(3)
    await message.edit(content=f"[**90.27%**] Selling data to the Goverment...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**93.12%**] Reporting account to Discord for breaking TOS...")
    await asyncio.sleep(3)
    await message.edit(content=f"[**95.70%**] Finished hacking {user}")
    await asyncio.sleep(3)
    await message.edit(content=f"[**100%**] The **totally** real and dangerous hack is complete")

@client.command()
async def greetdel(ctx,amount):
    if ctx.author.guild_permissions.manage_channels:
        servers = get_greet()
        valid = False
        try:
            for i in servers:
                if i[2] == ctx.channel.id:
                    update_greet(ctx.channel.id,int(amount))
                    embed = discord.Embed(description=f"<a:tick:867076348035989513> Seted greet announcement on: {amount}s", color=0x00FF00)
                    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
                    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
                    await ctx.channel.send(embed=embed)
                    valid = True
                    break
        except:
            valid=False
        if valid == False:
            embed = discord.Embed(description=f"<:no:867068050499305482> Greet command is not enabled on this channel", color=0xFF0000)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867076352149946388/download_12.jpg")
            await ctx.channel.send(embed=embed)

@client.command()
async def reedem(ctx, code):
    servers = get_premiumservers()
    is_server = False
    for i in servers:
      if i[1] == int(ctx.guild.id):
        is_server = True
        break
    codes = get_codes()
    valid = False
    if is_server == False:
        for i in codes:
          if str(i[1]) == str(code):
            remove_code(str(code))
            add_premium(int(ctx.guild.id))
            embed = discord.Embed(description=f"<a:tick:867076348035989513> Enabled premium on: {ctx.guild.name}", color=0x00FF00)
            embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
            embed.set_footer(text=f"Lunar•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/859872371842088981/860186039784439864/fd9a5fe710d981cd296503ccc4df0af5.gif?width=549&height=412")
            await ctx.channel.send(embed=embed)
            valid = True
        if valid == False:
          embed = discord.Embed(description=f"<a:deny:860216874163240961> Unknown code.", color=0xFF0000)
          embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
          embed.set_footer(text=f"Lunar•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/859872371842088981/860186039784439864/fd9a5fe710d981cd296503ccc4df0af5.gif?width=549&height=412")
          await ctx.channel.send(embed=embed)
    else:
        embed = discord.Embed(description=f"<:no:867068050499305482> This server already has premium.", color=0xFF0000)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/859872371842088981/860186039784439864/fd9a5fe710d981cd296503ccc4df0af5.gif?width=549&height=412")
        await ctx.channel.send(embed=embed)

@client.command()
async def devcode(ctx):
    if ctx.author.id == 852219497763045398:
        a = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        result = random.choices(a,k=5)
        codes = ""
        for i in result:
          codes += i
        add_code(codes)
        await ctx.author.send(f"**your code is:** `{codes}`")

@client.command()
async def premiumcodes(ctx):
    if ctx.author.id == 852219497763045398:
        codes = get_codes()
        await ctx.author.send(f"**Codes left:** `{codes}`")

@client.command()
@commands.has_permissions(administrator=True)
async def joinchannel(ctx, channel = None):
    if channel is None:
        embed2 = discord.Embed(description=f"Mention channel. | ,joinchannel #channel", color=0xFF0000)
        embed2.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed2.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed2)
    servers = get_join_channels()
    valid = False
    a = channel.replace("<#","").replace(">","")
    for i in servers:
        if i[2] == int(a):
          valid = True
          break
    if valid == False:
        add_joinchannel(ctx.guild.id,int(a))
        embed = discord.Embed(description=f"<a:tick:867076348035989513> Enabled joinchannel announcement on: {channel}", color=0x00FF00)
        embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed)
    else:
        embed1 = discord.Embed(description=f"<:no:867068050499305482> Join channel is already enabled. | write ,removejoinchannel to remove it.", color=0xFF0000)
        embed1.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
        embed1.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
        await ctx.channel.send(embed=embed1)

@client.command()
@commands.has_permissions(administrator=True)
async def removejoinchannel(ctx, channel):
    if channel is None:
      embed2 = discord.Embed(description=f"Mention channel. | ,joinchannel #channel", color=0xFF0000)
      embed2.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
      embed2.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
      await ctx.channel.send(embed=embed2)
    a = channel.replace("<#","").replace(">","")
    remove_joinchannel(int(a))
    embed = discord.Embed(description=f"<a:tick:867076348035989513> Removed join channel.", color=0x00FF00)
    embed.set_author(name=f"{ctx.author}",icon_url=f"{ctx.author.avatar_url}")
    embed.set_footer(text=f"Alpha•Todey {datetime.datetime.now().hour}:{datetime.datetime.now().minute}",icon_url="https://media.discordapp.net/attachments/867035975355858954/867270376861073428/download_12.jpg")
    await ctx.channel.send(embed=embed)

extensions = ['cogs.invites']
if __name__ == '__main__':
    for ext in extensions:
       client.load_extension(ext)

youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
             
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if not ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

client.add_cog(Music(client))

keep_alive.keep_alive()
client.run("ODYxODg2OTEyNjE2OTg4Njcy.YOQUvQ.zXgebLQo44vYupLeWZiv_7mhw7w")
