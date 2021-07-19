import asyncio
from asyncio.tasks import wait
import codingame
import discord
import random
from discord.colour import Color
from discord.ext import commands

bot = commands.Bot(command_prefix="!")
client = codingame.Client()

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")

@bot.event
async def on_ready():
    print('Le bot est pret')
    presences = ["!game to join a game", "!profile to get a profile", "coding ..."]
    while not bot.is_closed:
        presence = random.choice(presences)
        await bot.change_presence(activity=discord.Game(name=presence))
        await asyncio.sleep(6)

@bot.command(name="profile")
async def profile(ctx, arg):
    codingamer = client.get_codingamer(arg)
    embed = discord.Embed(title=codingamer.pseudo, url="https://www.codingame.com/profile/" + codingamer.public_handle, color=0xFF5733)
    embed.set_thumbnail(url=codingamer.avatar_url)
    await ctx.send(embed=embed)


@bot.command(name="game")
async def game(ctx):
    coc = client.get_pending_clash_of_code()
    embed = discord.Embed(title="Click to join", url=coc.join_url, description="**Players online:**", color=0xFF5733)
    embed.set_thumbnail(url="https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1410916443/e1aka8oyy6vnsbrt8ogw.png")
    for player in coc.players:
        embed.add_field(name=player.pseudo, value="https://www.codingame.com/profile/" + player.public_handle)
    embed.set_footer(text="Time before start: " + str(coc.time_before_start))
    await ctx.send(embed=embed)

bot.run("/")
