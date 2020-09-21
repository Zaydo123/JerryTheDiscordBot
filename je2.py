import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from itertools import cycle
import random

#variables
my_twitch_url = 'https://twitch.tv/turniphead_'
players = {}
client = commands.Bot(command_prefix = '/')
status = cycle(['Something','Videogames','GameSimulator','HumanSimulator','Boring Stuff','Funny Stuff', 'VALORANT', "COD", "World of Warcraft", "Minecraft", "Cow", "Im Confused", "Halo 3", "Moderation", "JerrySim2020","Night","SleepSimulator2020"])

#id = 719415051223826492




@client.event
async def on_ready():
    print("Bot is ready")
    async for guild in client.fetch_guilds(limit=150):
        print(guild.name)
        print("----------------------------------------")
    change_status.start()
#message on member join
@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')
    await member.guild.system_channel.send(f'{member} has joined the server!')
#message on member leave
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')
    await member.guild.system_channel.send(f'{member} has left the server')
#ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
    print("pong")
#clear
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=6):
    await ctx.channel.purge(limit=amount)
#kick
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
#ban
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
#unban
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member.discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

#userinfo
@client.command()
async def info(ctx, member:discord.Member):

    roles = [role for role in member.roles]

    embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild Name:", value=member.display_name)
    embed.add_field(name="Created At:", value=member.created_at.strftime("%a, %#d %B %Y %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


#status changer
@tasks.loop(seconds=40)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(next(status))))

#Hi there gif
@client.command(aliases=['hello', 'heythere', 'hey'])
async def hi(ctx):
    embed = discord.Embed(
        title = 'Hi',
        description= 'My name is Jerry',
        color = discord.Color.blue()
    )

    embed.set_image(url='https://media.giphy.com/media/3ogwFGEHrVxusDbDjO/giphy.gif')
    embed.set_author(name='Jerry', icon_url='https://cdn.discordapp.com/attachments/719415051223826495/741133048271339550/jerry.jpg')
    await ctx.send(embed=embed)

#awesome gif
@client.command()
async def awesome(ctx):
    embed = discord.Embed(
        title = 'Awesome!',
        color = discord.Color.blue()
    )
    embed.set_image(url='https://media.giphy.com/media/d2Z9QYzA2aidiWn6/giphy.gif')
    await ctx.send(embed=embed)


#online checker
@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if after.channel.id == 719421101402357910:
            await member.guild.system_channel.send("<@&741054769409425508>, someone is now playing Valorant")
            print("someone is playing valorant")

#print errors
@client.event
async def on_command_error(ctx,error):
    await ctx.send(f"There was an error with your command, please try again. {error}")
    print({error})

#coin flip
@client.command()
async def coin(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

#create member role
@client.command(aliases = ["cmr", "CMR"])
@commands.has_permissions(manage_roles=True)
async def creatememberrole(ctx, *, member:discord.Member):
    author = ctx.message.author
    guild = ctx.guild
    print(author.display_name)
    role = await guild.create_role(name=str(member.display_name))
    await member.add_roles(role)

#teams
@client.command(aliases=['teamsplit'])
async def team(ctx):
    team_select = discord.utils.get(ctx.guild.voice_channels, name='team-select')
    L0 = team_select.members
    team1 = discord.utils.get(ctx.guild.channels, name='team-1')
    team2 = discord.utils.get(ctx.guild.channels, name='team-2')
    user = random.choice(team_select.members)
    teamchoices = ["team1", "team2"]
    for i in L0:
        ranteam = random.choice(teamchoices)
        if ranteam == "team1":
            user = random.choice(team_select.members)
            await user.move_to(team1)
        elif ranteam == "team2":
            user = random.choice(team_select.members)
            await user.move_to(team2)

#team recall
@client.command(aliases=['tj', 'recall'])
async def teamjoin(ctx):
        team1 = discord.utils.get(ctx.guild.voice_channels, name='team-1')
        L0 = team1.members

        team_select = discord.utils.get(ctx.guild.channels, name='team-select')
        team1count = len(team1.members)
        team2 = discord.utils.get(ctx.guild.voice_channels, name='team-2')
        L1 = team2.members
        team2count = len(team2.members)

        if team2count + team1count >=0:
            for i in L0:
                user = random.choice(team1.members)
                await user.move_to(team_select)
            for i in L1:
                user = random.choice(team2.members)
                await user.move_to(team_select)
#=====================================================================================
@client.command()
@commands.has_permissions(manage_channels=True)
async def createteamchannels(ctx):
    guild = ctx.message.guild
    category = await guild.create_category("Teams")
    await guild.create_voice_channel(name='team-select', user_limit=10, overwrites=None, category=category, reason=None)
    await guild.create_voice_channel(name='team-1', user_limit=5, overwrites=None, category=category, reason=None)
    await guild.create_voice_channel(name='team-2', user_limit=5, overwrites=None, category=category, reason=None)

@client.command()
@commands.has_permissions(move_members=True)

def in_voice_channel():  # check to make sure ctx.author.voice.channel exists
    def predicate(ctx):
        return ctx.author.voice and ctx.author.voice.channel
    return check(predicate)

@in_voice_channel()
@client.command()
async def move(ctx, *, channel : discord.VoiceChannel):
    for members in ctx.author.voice.channel.members:
        await members.move_to(channel)





client.run('NzM4NTY3MTA3NzM3ODEzMDQy.XyNyOA.YV746l03m-d2YntLPHHyOlhT7B8')
