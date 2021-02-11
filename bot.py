import asyncio
import random
import discord
from discord.ext import commands
from discord.utils import async_all
from tox_block.prediction import make_single_prediction
import uuid

bot = commands.Bot(
	command_prefix="PH ",  
	case_insensitive=True,  
    description='ProvisionHacks Bot'
)

bot.remove_command('help')
bot.author_id = 408753256014282762 

@bot.event 
async def on_ready():  
    print("I'm in")
    print(bot.user)  
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Helping Hackers'))

  

@bot.command()
async def Ping(ctx):
    ping = round(bot.latency * 1000)
    await ctx.send(f"The ping of this bot is {ping} ms")

@bot.command()
async def Rules(ctx):
    embed = discord.Embed(description=f"```ProvisionHacks Rules```", color=0xAA83F9)
    embed.set_thumbnail(url="https://provisionhacks.com/assets/img/Frame%205.png")
    embed.add_field(name="MAX TEAM SIZE OF 4",
                    value="Teams can be composed of no more than 4 people", inline=False)
    embed.add_field(name="NO STARTING IN ADVANCE",
                    value="All coding, designing, etc. for your project must be developed during the event only. Although you may not begin coding in advance, you may discuss and plan in advance with teammates. ", inline=False)
    embed.add_field(name="NO USING PAST PROJECTS",
                    value="You are not allowed to use projects from previous hackathons nor continue working on a project from a previous hackathon.", inline=False)
    embed.add_field(name="BE RESPECTFUL",
                    value="You must be respectful to the other participants and attendees. If a problem occurs please make sure to reach out to the Provision Hacks Organizers.", inline=False)
    embed.add_field(name="MLH CODE OF CONDUCT",
                    value="Please make sure that you read and comply with the MLH Code of Conduct", inline=False)
    embed.add_field(name="QUESTIONS?",
                    value="For any other questions or concerns, DM one of the organizers or reach us at info@provisionhacks.com", inline=False)
    embed.set_footer(text="info@provisionhacks.com")
    await ctx.send(embed = embed)
    
@bot.event
async def on_member_join(member):
    channel = await member.create_dm()
    embed = discord.Embed(
        title=f"Welcome to {member.guild.name}",
        description=f"ProvisionHacks is a 24 student led hackathon.",
        color=0x83DCF9)
    embed.add_field(name="MAX TEAM SIZE OF 4",
                    value="Teams can be composed of no more than 4 people", inline=False)
    embed.add_field(name="NO STARTING IN ADVANCE",
                    value="All coding, designing, etc. for your project must be developed during the event only. Although you may not begin coding in advance, you may discuss and plan in advance with teammates. ", inline=False)
    embed.add_field(name="NO USING PAST PROJECTS",
                    value="You are not allowed to use projects from previous hackathons nor continue working on a project from a previous hackathon.", inline=False)
    embed.add_field(name="BE RESPECTFUL",
                    value="You must be respectful to the other participants and attendees. If a problem occurs please make sure to reach out to the Provision Hacks Organizers.", inline=False)
    embed.add_field(name="MLH CODE OF CONDUCT",
                    value="Please make sure that you read and comply with the MLH Code of Conduct", inline=False)
    embed.add_field(name="QUESTIONS?",
                    value="For any other questions or concerns, DM one of the organizers or reach us at info@provisionhacks.com", inline=False)
    embed.set_footer(text="info@provisionhacks.com")
    embed.set_footer(text="ProvisionHacks")
    await channel.send(embed=embed)
    
@bot.event
async def on_message(message):
    try:
            role = discord.utils.find(lambda r: r.name == 'Muted', message.guild.roles)
            if role in message.author.roles:
                await message.delete()
    except:
        pass
    try:
        aimessage = make_single_prediction(message.content, rescale=True)
        toxic = aimessage["toxic"]  
        severe_toxic = aimessage["severe_toxic"]
        obscene = aimessage["obscene"]
        threat = aimessage["threat"]
        insult = aimessage["insult"]
        if round(toxic, 2) > 0.8:
            embed = discord.Embed(title=f"**{message.author}**",description=f"```{message.content}```", color=0xFFCD00)
            embed.set_thumbnail(url="https://provisionhacks.com/assets/img/Frame%205.png")
            embed.add_field(name="Toxic",
                            value=str(round(toxic, 2)), inline=False)
            embed.add_field(name="Severe Toxic",
                            value=str(round(severe_toxic, 2)), inline=False)
            embed.add_field(name="Insult",
                            value=str(round(insult, 2)), inline=False)
            embed.add_field(name="Obscene",
                            value=str(round(obscene, 2)), inline=False)
            embed.add_field(name="Threat",
                            value=str(round(threat, 2)), inline=False)
            embed.set_footer(text="PROVISION HACKS")
            channel = bot.get_channel(808533470342545459)
            await channel.send(embed = embed)
        else:
            print(f'Approved {round(toxic, 2)}')
    except:
        pass
    if message.channel.id == 809457179903393803:
        await message.author.edit(nick=f"{message.content}")
        rolee = discord.utils.get(message.guild.roles, name=f"Hackers")
        await message.author.add_roles(rolee)
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction)
    if reaction.emoji == "❓":
        ticketID = uuid.uuid1()
        guild = reaction.message.guild
        category = discord.utils.get(guild.categories, name="Support-Ticket")
        overwrites = {
            guild.default_role:
            discord.PermissionOverwrite(view_channel=False),
            guild.me: discord.PermissionOverwrite(view_channel=True),
            user: discord.PermissionOverwrite(view_channel=True),
        }
        
        await guild.create_text_channel(f'ticket-{ticketID}',category=category, overwrites=overwrites)
        newchannel = discord.utils.get(guild.channels, name=f'ticket-{ticketID}')
        await newchannel.send("Your support ticker has been created! Please wait as one of the <@&784137002286448682> will get to you shortly")
    if reaction.emoji == "👍":
        rolee = discord.utils.get(reaction.message.guild.roles, name=f"Hackers")
        await user.add_roles(rolee)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f'{error}')

bot.run("ODA4NTIzMzAwMzM0MzM4MTM5.YCHyAA.tWX1GllwEDdo1fNXyWuMS8VmKqk")  # Starts the bot